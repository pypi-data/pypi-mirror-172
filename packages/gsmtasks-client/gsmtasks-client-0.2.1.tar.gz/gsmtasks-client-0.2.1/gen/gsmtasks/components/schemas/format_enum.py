from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class FormatEnum(enum.Enum):
    json = "json"
    xlsx = "xlsx"
