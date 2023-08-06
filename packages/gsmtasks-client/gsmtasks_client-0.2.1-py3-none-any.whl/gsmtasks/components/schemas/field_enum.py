from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class FieldEnum(enum.Enum):
    state = "state"
    assignee_proximity = "assignee_proximity"
