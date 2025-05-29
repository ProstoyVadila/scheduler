import asyncio
import os
import datetime

from loguru import logger
from redis import Redis

from scheduler.io.cache import Cache
from scheduler.task_worker.pollers.cache import poll_cache
from scheduler.task_worker.pollers.database import poll_database

async def init() -> None:
    """
    Initialize the task worker.
    This function is called when the application starts up.
    It can be used to perform startup tasks.
    """
    # Perform startup tasks here
    logger.info("Initializing task worker...")

    cache = Cache()
    # Start the cache poller
    cache_poller = asyncio.create_task(poll_cache(cache))
    # Start the database poller
    database_poller = asyncio.create_task(poll_database(cache))

    try:
        await asyncio.gather(cache_poller, database_poller, return_exceptions=True)
    except Exception as e:
        logger.error(f"Error in task worker: {e}")
        raise 


async def shutdown() -> None:
    """
    Shutdown the task worker.
    This function is called when the application shuts down.
    It can be used to perform shutdown tasks.
    """
    # Perform shutdown tasks here
    logger.info("Shutting down task worker...")
    await asyncio.sleep(1)
    logger.info("Task worker has shut down")
    # Cleanup tasks here
    # e.g., close database connections, stop background tasks, etc.