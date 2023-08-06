from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class LevelEnum(enum.Enum):
    danger = "danger"
    warning = "warning"
    success = "success"
