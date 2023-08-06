from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TimeLocationStateEnum(enum.Enum):
    unknown = "unknown"
    stopped = "stopped"
    moving = "moving"
