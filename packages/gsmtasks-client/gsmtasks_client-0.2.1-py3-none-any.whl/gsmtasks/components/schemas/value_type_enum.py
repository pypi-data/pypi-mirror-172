from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class ValueTypeEnum(enum.Enum):
    string = "string"
    integer = "integer"
    decimal = "decimal"
    choice = "choice"
