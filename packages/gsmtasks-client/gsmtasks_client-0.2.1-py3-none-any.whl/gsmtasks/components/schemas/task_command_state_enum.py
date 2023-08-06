from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TaskCommandStateEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
