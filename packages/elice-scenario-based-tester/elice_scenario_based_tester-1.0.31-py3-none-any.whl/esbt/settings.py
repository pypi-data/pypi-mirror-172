from typing import Any

from pydantic import BaseSettings, Field


class WorkflowSettings(BaseSettings):
    RESPONSE_VERIFY_DICT: dict[str, dict[str, Any]] = Field(
        default={
            "127.0.0.1:6663": {"_result.status": "ok"}
        },
        description="Response validation for API server.",
    )

    class Config:
        env_file = ".env.esbt"
        env_prefix = "esbt_"
