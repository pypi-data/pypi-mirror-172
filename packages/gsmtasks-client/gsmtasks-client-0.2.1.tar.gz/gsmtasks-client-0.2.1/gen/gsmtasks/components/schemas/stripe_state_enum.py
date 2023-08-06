from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class StripeStateEnum(enum.Enum):
    requires_payment_method = "requires_payment_method"
    requires_confirmation = "requires_confirmation"
    requires_capture = "requires_capture"
    requires_action = "requires_action"
    processing = "processing"
    succeeded = "succeeded"
    canceled = "canceled"
