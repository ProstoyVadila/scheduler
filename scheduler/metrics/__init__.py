import os
from typing import Callable

from loguru import logger

MULTIPROCESS_METRICS_DIR = "tmp/metrics"


def cleanup_metrics_folder() -> None:
    """
    Cleanup function to remove the metrics directory.
    This function is called when the application shut down or starts up (just in case).
    """
    if os.path.exists(MULTIPROCESS_METRICS_DIR):
        for filename in os.listdir(MULTIPROCESS_METRICS_DIR):
            file_path = os.path.join(MULTIPROCESS_METRICS_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                logger.error(f"Failed to delete previous metrics {file_path}. Reason: {e}")
    else:
        logger.warning(f"Metrics directory {MULTIPROCESS_METRICS_DIR} does not exist")
    logger.info("Metrics directory cleaned up")


def prepare(workers: int) -> Callable:
    if workers > 1:
        if not os.path.exists(MULTIPROCESS_METRICS_DIR):
            os.makedirs(MULTIPROCESS_METRICS_DIR)
        else:
            cleanup_metrics_folder()
        # It's crucial to set that environment variable before prometheus_fastapi_instrumentator is started
        # because it will use it to set the metrics directory for the multiprocess mode.
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = MULTIPROCESS_METRICS_DIR
        logger.info(f"Metrics directory set to {MULTIPROCESS_METRICS_DIR}")
