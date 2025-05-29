import os

def get_workers(reserved_workers: int = 0) -> int:
    """
    Get the number of workers to use for the server.
    It is believed the most effiecient amount of workers should be 2 * (number of CPU cores) + 1.
    """
    workers = os.getenv("WORKERS") or 2 * (os.cpu_count() or 1) + 1
    return max(int(workers) - reserved_workers, 2)
