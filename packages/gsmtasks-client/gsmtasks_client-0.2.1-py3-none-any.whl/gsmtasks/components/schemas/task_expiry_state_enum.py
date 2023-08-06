from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TaskExpiryStateEnum(enum.Enum):
    cancelled = "cancelled"
    completed = "completed"
