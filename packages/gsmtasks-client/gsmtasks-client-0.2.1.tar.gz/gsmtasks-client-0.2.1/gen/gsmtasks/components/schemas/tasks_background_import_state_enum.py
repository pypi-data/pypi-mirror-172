from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TasksBackgroundImportStateEnum(enum.Enum):
    pending = "pending"
    started = "started"
    completed = "completed"
    failed = "failed"
