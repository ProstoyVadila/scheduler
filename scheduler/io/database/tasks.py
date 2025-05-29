# TODO: Implement the TasksRepository class
from datetime import datetime

from sqlalchemy import select, insert, update, inspect
from loguru import logger

from scheduler.io.database.base import BaseRepository
from scheduler.models.view.tasks import TaskStatus
from scheduler.models.table.tasks import TaskTable


def sa_to_dict(task: TaskTable) -> dict[str, any]:
    return {
        c.key: getattr(task, c.key)
        for c in inspect(task).mapper.column_attrs
    }


class TasksRepository(BaseRepository):
    """
    Repository class for managing tasks in the database.
    This class provides methods to interact with the tasks table.
    """

    def __init__(self, session=None) -> None:
        """
        Initialize the TasksRepository with an async session.

        Args:
            session (async_sessionmaker | None): The async session to use for database operations.
        """
        super().__init__(session=session)
        self._table_name = TaskTable.__tablename__
        self._table_alias = "t"
        self.table = TaskTable

    async def get_task_by_id(self, task_id: int) -> TaskTable | None:
        """
        Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            TaskTable | None: The task object if found, otherwise None.
        """
        stmt = select(self.table).where(self.table.id == task_id)
        result = await self.execute_with_retries(stmt)
        return result.scalar_one_or_none()

    async def get_tasks_by_datetime(self, start: datetime, end: datetime) -> list[TaskTable]:
        """
        Get tasks by their scheduled datetime.

        Args:
            start (int): The start datetime in milliseconds.
            end (int): The end datetime in milliseconds.

        Returns:
            list[TaskTable]: A list of task objects within the specified datetime range.
        """
        stmt = select(self.table).where(
            self.table.next_run >= start,
            self.table.next_run <= end
        )
        result = await self.execute_with_retries(stmt)
        return result.scalars().all()

    async def update_task_status(self, task_id: int, status: TaskStatus) -> None:
        """
        Update the status of a task.

        Args:
            task_id (int): The ID of the task to update.
            status (TaskStatus): The new status to set for the task.

        Returns:
            None
        """
        stmt = (
            update(self.table)
            .where(self.table.id == task_id)
            .values(status=status)
        )
        await self.execute_with_retries(stmt)
        logger.debug(f"Task {task_id} status has been updated to {status}")

    async def create_task(self, task: TaskTable) -> TaskTable:
        """
        Create a new task in the database or update it if it already exists.

        Args:
            task (TaskTable): The task object to create or update.

        Returns:
            TaskTable: The created or updated task object.
        """
        try:
            stmt = insert(self.table).values(
                name=task.name,
                description=task.description,
                cron=task.cron,
                command=task.command,
                status=task.status,
                enabled=task.enabled,
                last_run=task.last_run,
                next_run=task.next_run,
                retries=task.retries,
                max_retries=task.max_retries,
                error_message=task.error_message,
            )
            # .on_conflict_do_update(
            #     index_elements=[self.table.id],  # Specify the unique constraint or index
            #     set_={
            #         "name": task.name,
            #         "description": task.description,
            #         "cron": task.cron,
            #         "command": task.command,
            #         "status": task.status,
            #         "enabled": task.enabled,
            #         "last_run": task.last_run,
            #         "next_run": task.next_run,
            #         "retries": task.retries,
            #         "max_retries": task.max_retries,
            #         "error_message": task.error_message,
            #     }
            # )
            await self.execute_with_retries(stmt)
            logger.debug(f"Task {task.name} has been created or updated in the database")
            # Fetch the created or updated task from the database
            created_task = await self.get_task_by_id(task.id)
            return created_task
        except Exception as e:
            # Log the exception or handle it as needed
            raise RuntimeError(f"Failed to create or update task: {e}") from e
