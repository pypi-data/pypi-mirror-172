from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TaskCategoryEnum(enum.Enum):
    assignment = "assignment"
    pick_up = "pick_up"
    drop_off = "drop_off"
    warehouse = "warehouse"
