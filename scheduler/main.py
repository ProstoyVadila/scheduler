import asyncio
import os
import multiprocessing

import uvicorn
from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from scheduler.lifespan import lifespan
from scheduler import metrics
from scheduler.utils.workers import get_workers
from scheduler.api.routers.default import default_router
from scheduler.api.routers.tasks import tasks_router
from scheduler import task_worker


app = FastAPI(
    title="Scheduler API",
    description="API for scheduling tasks",
    version="0.0.1",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

app.include_router(default_router, tags=["default"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


def run_fastapi() -> None:
    workers = get_workers()
    metrics.prepare(workers)
    logger.info(f"Starting server with {workers} workers")
    uvicorn.run(
        "scheduler.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=os.getenv("APP_PORT", 8080),
        workers=workers
    )


def run_task_worker() -> None:
    try:
        logger.info("Starting task worker...")
        asyncio.run(task_worker.init())
        logger.info("Task worker started successfully")
    except KeyboardInterrupt:
        logger.info("Task worker interrupted by user")
    except Exception as e:
        logger.error(f"Error in task worker: {e}")
        raise
    finally:
        asyncio.run(task_worker.shutdown())
        logger.info("Task worker has shut down")


if __name__ == "__main__":
    worker_process = multiprocessing.Process(target=run_task_worker)
    worker_process.start()
    logger.info(f"Task worker started with PID: {worker_process.pid}")

    run_fastapi()

    worker_process.join()
    logger.info("Task worker has shut down")
