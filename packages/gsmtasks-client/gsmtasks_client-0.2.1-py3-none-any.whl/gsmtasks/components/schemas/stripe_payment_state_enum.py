from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class StripePaymentStateEnum(enum.Enum):
    draft = "draft"
    failed = "failed"
    saved = "saved"
    settled = "settled"
    rejected = "rejected"
    retried = "retried"
    cancelled = "cancelled"
