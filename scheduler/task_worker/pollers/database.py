import asyncio
import os
import datetime

import orjson
from loguru import logger

from scheduler.io.cache import Cache
from scheduler.utils.timestamp import get_millisecond_timestamp, get_current_millisecond_timestamp

from scheduler.models.table.tasks import TaskTable
from scheduler.models.view.tasks import Task
from scheduler.io.database.tasks import TasksRepository, sa_to_dict


# Intervals for polling in seconds
DATABASE_POLL_INTERVAL = 60

TASKS_SET = "tasks"

async def _poll_database(cache: Cache, task_repo: TasksRepository) -> None:
    """
    Poll the database for tasks and schedule them in the cache.
    
    Args:
        cache (Cache): The cache client to use for scheduling tasks.
    
    Returns:
        None
    """
    # Perform startup tasks here
    logger.warning("Initializing database poller...")
    # Simulate database connection
    await asyncio.sleep(1)
    logger.warning("Database client is initialized successfully")
    if task_repo is None:
        task_repo = TasksRepository()

    while True:
        cache_client = await cache.get_conn()
        # now = get_current_millisecond_timestamp()
        now = datetime.datetime.now(tz=datetime.UTC)
        end = now + datetime.timedelta(seconds=DATABASE_POLL_INTERVAL * 10)
        tasks = await task_repo.get_tasks_by_datetime(
            start=now,
            end=end,
        )
        if tasks:
            for task in tasks:
                task_data = sa_to_dict(task)
                task_payload = orjson.dumps({"task_id": task.id, "task_data": task_data}).decode("utf-8")
                await cache_client.zadd(TASKS_SET, {task_payload: task.next_run.timestamp()})
                logger.info(f"Task {task} has been scheduled")
        else:
            logger.debug("No tasks to schedule")
        await asyncio.sleep(DATABASE_POLL_INTERVAL * 3 / 4)


async def poll_database(cache: Cache) -> None:
    try:
        task_repo = TasksRepository()
        await _poll_database(cache, task_repo)
    except KeyboardInterrupt:
        logger.info("Database poller stopped by user")
    except SystemExit:
        logger.info("Database poller stopped by system exit")
    except asyncio.CancelledError:
        logger.info("Database poller cancelled")
    except Exception as e:
        logger.error(f"Unexpected error in database poller: {e}")
        await asyncio.sleep(DATABASE_POLL_INTERVAL)
        await poll_database(cache)
