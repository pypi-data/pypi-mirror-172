from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TimeFormatEnum(enum.Enum):
    HH_mm = "HH:mm"
    h_mm_A = "h:mm A"
