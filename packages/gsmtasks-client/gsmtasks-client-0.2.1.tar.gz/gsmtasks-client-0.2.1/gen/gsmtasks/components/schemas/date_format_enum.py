from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class DateFormatEnum(enum.Enum):
    dmy_dot = "DD.MM.YYYY"
    dmy_slash = "DD/MM/YYYY"
    iso = "YYYY-MM-DD"
    MM_DD_YYYY = "MM/DD/YYYY"
