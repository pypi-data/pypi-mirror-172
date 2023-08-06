from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class RouteOptimizationSerializerV2StateEnum(enum.Enum):
    pending = "pending"
    started = "started"
    ready = "ready"
    completed = "completed"
    over_quota = "over_quota"
    failed = "failed"
