from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class ObjectiveEnum(enum.Enum):
    vehicles = "vehicles"
    transport_time = "transport_time"
    completion_time = "completion_time"
