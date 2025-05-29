import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


def get_async_session() -> async_sessionmaker:
    """
    Create an asynchronous sessionmaker for the database.
    This function is called when the application starts up.
    It can be used to perform startup tasks.
    """
    engine = create_async_engine(
        os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/schedb"),
        echo=True,
        # future=True,
        pool_size=10,
        pool_pre_ping=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)
