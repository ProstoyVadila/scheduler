# scheduler/io/database/models/task_table.py
from datetime import datetime, timezone
from enum import StrEnum, auto


from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    Boolean,
    Enum,
)
from sqlalchemy.orm import declarative_base

from scheduler.models.view.tasks import TaskStatus

Base = declarative_base()

class TaskTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    cron = Column(String(255), nullable=True)
    command = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.SCHEDULED)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime(timezone=True), nullable=True)
    next_run = Column(DateTime(timezone=True), nullable=True)
    retries = Column(Integer, default=0)
    max_retries = Column(Integer, default=5)
    error_message = Column(Text, nullable=True)