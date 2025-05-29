from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """Base configuration settings."""

    # General settings
    app_name: str = Field("SchedulerApp", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


class SchedulerConfig(BaseConfig):
    """Scheduler configuration settings."""

    # Scheduler settings
    scheduler_interval: int = Field(60, env="SCHEDULER_INTERVAL")  # in seconds
    max_concurrent_jobs: int = Field(20, env="MAX_CONCURRENT_JOBS")
    