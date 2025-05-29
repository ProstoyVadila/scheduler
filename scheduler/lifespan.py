import os
import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from loguru import logger
from fastapi import FastAPI

from scheduler import task_worker
from scheduler.io.cache import Cache
from scheduler.task_worker.pollers import TASKS
from scheduler.models.table.tasks import TaskTable
from scheduler.io.database.tasks import TasksRepository


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan context manager for FastAPI application.
    This function is called when the application starts up and shuts down.
    It can be used to perform startup and shutdown tasks.
    """
    # Perform startup tasks here
    logger.info("Starting up...")

    # Initialize the cache
    # logger.info("Initializing cache...")
    

    # logger.info("Cache initialized successfully")

    # Initialize the task worker
    # logger.info("Initializing task worker...")
    # asyncio.create_task(task_worker.init())

    task_repository = TasksRepository()
    logger.warning("Creating tasks...")
    for task in TASKS:
        task_table = TaskTable(**task)
        result = await task_repository.create_task(task_table)
        logger.warning(f"Task {result} created with ID {type(result)}")

    yield

    # Perform shutdown tasks here
    # logger.info("Shutting down task worker...")
    # await task_worker.shutdown()
    # logger.info("Task worker has shut down")

    # Shutdown the cache
    # logger.info("Shutting down cache...")

    # logger.info("Cache has shut down")

    # Perform shutdown tasks here
    logger.info("Shutting down...")
