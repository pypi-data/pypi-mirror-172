from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class AccountBillingMethodEnum(enum.Enum):
    braintree = "braintree"
    free = "free"
    invoice = "invoice"
    stripe = "stripe"
    trial = "trial"
