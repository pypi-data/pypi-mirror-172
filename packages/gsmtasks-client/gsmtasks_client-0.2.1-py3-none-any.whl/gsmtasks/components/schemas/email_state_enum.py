from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class EmailStateEnum(enum.Enum):
    queued = "queued"
    over_quota = "over_quota"
    sent = "sent"
    failed = "failed"
    received = "received"
