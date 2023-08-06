from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class StatusEnum(enum.Enum):
    on_duty = "on_duty"
    off_duty = "off_duty"
