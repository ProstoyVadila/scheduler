from enum import StrEnum, auto
import datetime

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(StrEnum):
    """Task status enumeration."""
    SCHEDULED = auto()  # Task is scheduled but not yet executed
    CACHED = auto()  # prepared (stored in cache) before execution
    RUNNING = auto()
    SUCCESS = auto()  # all tasks are completed successfully
    FAILED = auto()


class CustomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     """Pydantic model configuration."""
    #     # orm_mode = True
    #     # use_enum_values = True
    #     from_attributes = True

class Task(BaseModel):
    id: int = Field(..., title="Task ID", description="Unique identifier for the task")
    name: str = Field(..., title="Task Name", description="Name of the task")
    description: str = Field(..., title="Task Description", description="Description of the task")
    cron: str = Field(..., title="Cron Expression", description="Cron expression for scheduling the task")
    command: str = Field(..., title="Command", description="Command to be executed by the task")
    status: TaskStatus = Field(default=TaskStatus.SCHEDULED, title="Task Status", description="Current status of the task")
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), title="Creation Time", description="Time when the task was created")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), title="Last Updated Time", description="Time when the task was last updated")
    enabled: bool = Field(default=True, title="Enabled", description="Whether the task is enabled or disabled")
    last_run: datetime.datetime | None = Field(default=None, title="Last Run Time", description="Time when the task was last run")
    next_run: datetime.datetime | None = Field(default=None, title="Next Run Time", description="Time when the task is next scheduled to run")
    retries: int = Field(default=0, title="Retries", description="Number of retries attempted for the task")
    max_retries: int = Field(default=5, title="Max Retries", description="Maximum number of retries allowed for the task")
    error_message: str | None = Field(default=None, title="Error Message", description="Error message if the task fails")
    # Add any additional fields as needed
