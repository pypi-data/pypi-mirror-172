from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class PushNotificationStateEnum(enum.Enum):
    queued = "queued"
    pending = "pending"
    failed = "failed"
    sent = "sent"
