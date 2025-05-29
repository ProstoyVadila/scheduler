

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import TextClause, Result
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from scheduler.io.database.session import get_async_session
from scheduler.utils.exceptions import RetryError

from scheduler.utils.timer import timer


class BaseRepository:
    """
    Base repository class for database operations.
    This class provides a base for all repositories to inherit from.
    It contains common methods for database operations.
    """

    def __init__(self, session: async_sessionmaker | None = None, max_attemps: int = 20, max_wait: float = 1.2) -> None:
        """
        Initialize the BaseRepository with an async session.

        Args:
            session (async_sessionmaker | None): The async session to use for database operations.
            max_attemps (int): Maximum number of attempts to establish a connection.
            max_wait (float): Maximum wait time between attempts in seconds.
        """
        self.session: async_sessionmaker = session or get_async_session()
        self._max_attempts = max_attemps
        self._max_wait = max_wait

    @timer
    async def _execute(self, statement: TextClause, params: dict | None = None) -> Result:
        """
        Execute a SQL statement with retries.

        Args:
            statement (TextClause): The SQL statement to execute.
            params (dict | None): The parameters for the SQL statement.

        Returns:
            ResultProxy: The result of the SQL statement execution.
        """
        async with self.session() as session:
            result = await session.execute(statement, params)
            await session.commit()  # Commit the transaction after execution
            return result


    async def execute_with_retries(self, statement: TextClause, params: dict | None = None) -> Result:
        """
        Execute a SQL statement with retries.

        Args:
            statement (TextClause): The SQL statement to execute.
            params (dict | None): The parameters for the SQL statement.

        Returns:
            ResultProxy: The result of the SQL statement execution.
        """
        last_exception: Exception | None = None
        attempts = 1
        wait = 0.1
        while attempts < self._max_attempts:
            try:
                 return await self._execute(statement, params)
            except SQLAlchemyError as e:
                last_exception = e
                retry = f"Retrying user-service call in {wait} as it raised {type(e)}"
                msg = f"Attempt # {attempts} failed. {retry}"
                logger.exception(msg)
                await asyncio.sleep(min(wait, self._max_wait))
                wait *= 2
                attempts += 1
        if last_exception is None:
            msg = f"Attempt # {attempts} failed but with no last exception!"
            raise RetryError(msg)
        raise RetryError(f"Attempt # {attempts} failed") from last_exception
