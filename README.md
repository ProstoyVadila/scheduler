# Scheduler

An example of a scheduler using FastAPI for running tasks at specified intervals using PostgreSQL as the task storage and Redis for caching expiring tasks before execution. It includes cache to be more precise about execution times and to avoid unnecessary database queries.
