import os
import asyncio

from loguru import logger
from redis import asyncio as aioredis

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = 0
REDIS_RETRY_ATTEMPTS = 5
REDIS_RETRY_DELAY = 2  # Seconds
REDIS_SOCKET_TIMEOUT = 5  # Seconds

cache_client: aioredis.Redis | None = None


# async def get_client() -> None:
#     """
#     Initialize the cache.
#     This function is called when the application starts up.
#     It can be used to perform startup tasks.
#     """
#     # Perform startup tasks here
#     for attempt in range(1, REDIS_RETRY_ATTEMPTS + 1):
#         try:
#             cache_client = await aioredis.from_url(
#                 f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
#                 retry_on_timeout=True,
#                 decode_responses=True,
#                 socket_connect_timeout=REDIS_SOCKET_TIMEOUT,
#                 socket_timeout=REDIS_SOCKET_TIMEOUT,
#                 encoding="utf-8",
#             )
#             await cache_client.ping()
#             logger.info("Successfully connected to Redis")
#             return cache_client
#         except Exception as e:
#             logger.error(f"Attempt {attempt} to connect to Redis failed: {e}")
#             if attempt < REDIS_RETRY_ATTEMPTS:
#                 logger.info(f"Retrying in {REDIS_RETRY_DELAY} seconds...")
#                 await asyncio.sleep(REDIS_RETRY_DELAY)
#             else:
#                 logger.error("Exceeded maximum retry attempts to connect to Redis")
#                 raise RuntimeError("Cache initialization failed") from e


# async def close() -> None:
#     """
#     Shutdown the cache.
#     This function is called when the application shuts down.
#     It can be used to perform shutdown tasks.
#     """
#     # Perform shutdown tasks here
#     global cache_client
#     if cache_client is None:
#         logger.warning("Cache client is already closed or not initialized")
#         return
#     await cache_client.close()
#     logger.info("Cache client closed successfully")
#     cache_client = None

class Cache:
    def __init__(self):
        self._client: aioredis.Redis | None = None

    async def get_conn(self) -> aioredis.Redis:
        """
        Get a Redis connection. Reuse the existing connection or create a new one.
        """
        if self._client:
            return self._client

        for attempt in range(1, REDIS_RETRY_ATTEMPTS + 1):
            try:
                self._client = await aioredis.from_url(
                    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
                    retry_on_timeout=True,
                    decode_responses=True,
                    socket_connect_timeout=REDIS_SOCKET_TIMEOUT,
                    socket_timeout=REDIS_SOCKET_TIMEOUT,
                    encoding="utf-8",
                )
                await self._client.ping()
                logger.info("Successfully connected to Redis")
                return self._client
            except Exception as e:
                logger.error(f"Attempt {attempt} to connect to Redis failed: {e}")
                if attempt < REDIS_RETRY_ATTEMPTS:
                    logger.info(f"Retrying in {REDIS_RETRY_DELAY} seconds...")
                    await asyncio.sleep(REDIS_RETRY_DELAY)
                else:
                    logger.error("Exceeded maximum retry attempts to connect to Redis")
                    raise RuntimeError("Cache initialization failed") from e

    async def close(self) -> None:
        """
        Close the Redis connection gracefully.
        """
        if self._client is None:
            logger.warning("Cache client is already closed or not initialized")
            return
        await self._client.close()
        logger.info("Cache client closed successfully")
        self._client = None
