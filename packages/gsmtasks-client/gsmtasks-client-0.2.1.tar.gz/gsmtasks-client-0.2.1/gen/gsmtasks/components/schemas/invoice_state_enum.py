from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class InvoiceStateEnum(enum.Enum):
    draft = "draft"
    confirmed = "confirmed"
    overdue = "overdue"
    paid = "paid"
    cancelled = "cancelled"
