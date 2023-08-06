from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class Type21dEnum(enum.Enum):
    service = "service"
    delivery = "delivery"
