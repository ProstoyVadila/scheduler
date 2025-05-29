import asyncio
import datetime

from loguru import logger

from scheduler.io.cache import Cache
from scheduler.utils.timestamp import get_current_millisecond_timestamp



# Intervals for polling in seconds
CACHE_POLL_INTERVAL = 1
DATABASE_POLL_INTERVAL = 60

TASKS_SET = "tasks"


# TODO: add try except for all async functions and error handling


async def _poll_cache(cache: Cache) -> None:
        # Perform startup tasks here
    logger.info("Initializing cache poller...")

    # cache_client = await cache.get_client()
    logger.info("Cache client is initialized successfully")
    
    while True:
        await asyncio.sleep(CACHE_POLL_INTERVAL * 3 / 4)
        cache_conn = await cache.get_conn()
        now = get_current_millisecond_timestamp(plus_dt=datetime.timedelta(seconds=CACHE_POLL_INTERVAL))
        # TODO: use custom funcs with retry wrapper
        tasks = await cache_conn.zrangebyscore(
            name=TASKS_SET,
            min=0,
            max=now,
        )
        if tasks:
            for task in tasks:
                # Simulate task execution
                logger.debug(f"Executing task: {task}")
                await cache_conn.zrem(TASKS_SET, task)
                logger.info(f"Task {task} has been executed and removed from the queue")
        else:
            logger.debug("No tasks to execute")


async def poll_cache(cache: Cache) -> None:
    try:
        await _poll_cache(cache)
    except KeyboardInterrupt:
        logger.info("Cache poller stopped by user")
    except SystemExit:
        logger.info("Cache poller stopped by system exit")
    except asyncio.CancelledError:
        logger.info("Cache poller cancelled")
    except Exception as e:
        logger.error(f"Unexpected error in cache poller: {e}")
        await asyncio.sleep(CACHE_POLL_INTERVAL)
        await poll_cache(cache)
    finally:
        logger.info("Cache poller shutting down")
        await cache.close()
        logger.info("Cache poller has shut down")