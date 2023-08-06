from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class DistanceUnitsEnum(enum.Enum):
    kilometers = "kilometers"
    miles = "miles"
