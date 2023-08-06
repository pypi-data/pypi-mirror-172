from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class MethodEnum(enum.Enum):
    app = "app"
    email = "email"
    sms = "sms"
