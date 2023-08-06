from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class InvoiceBillingMethodEnum(enum.Enum):
    braintree = "braintree"
    invoice = "invoice"
    stripe = "stripe"
