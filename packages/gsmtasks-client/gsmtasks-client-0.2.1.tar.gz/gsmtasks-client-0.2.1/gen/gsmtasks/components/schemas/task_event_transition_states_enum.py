from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TaskEventTransitionStatesEnum(enum.Enum):
    unassigned = "unassigned"
    assigned = "assigned"
    accepted = "accepted"
    transit = "transit"
    active = "active"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    away = "away"
    near = "near"
