from fastapi import APIRouter
from pydantic import ValidationError

from scheduler.models.view.tasks import Task
from scheduler.models.table.tasks import TaskTable
from scheduler.io.database.tasks import TasksRepository

tasks_router = APIRouter()
tasks_repository = TasksRepository()


@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Get a task by its ID.
    
    Args:
        task_id (int): The ID of the task to retrieve.
    
    Returns:
        Task: The task object if found, otherwise None.
    """
    task = await tasks_repository.get_task_by_id(task_id)
    if task is None:
        return {"error": "Task not found"}
    try:
        return Task.model_validate(task)
    except ValidationError as e:
        return {"error": "Validation error", "details": e.errors()}


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    """
    Create a new task in the database.
    
    Args:
        task (Task): The task object to create.
    
    Returns:
        Task: The created task object.
    """
    try:
        task = TaskTable(**task.model_dump())
        created_task = await tasks_repository.create_task(task)
        return Task.model_validate(created_task)
    except ValidationError as e:
        return {"error": "Validation error", "details": e.errors()}