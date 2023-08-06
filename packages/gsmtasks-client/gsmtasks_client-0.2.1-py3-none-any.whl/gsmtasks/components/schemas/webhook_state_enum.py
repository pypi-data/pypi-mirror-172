from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class WebhookStateEnum(enum.Enum):
    inactive = "inactive"
    active = "active"
    disabled = "disabled"
