from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class RecipientEnum(enum.Enum):
    account = "account"
    assignee = "assignee"
    orderer = "orderer"
    contact = "contact"
    client = "client"
