from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class AssigneeProximityEnum(enum.Enum):
    away = "away"
    near = "near"
