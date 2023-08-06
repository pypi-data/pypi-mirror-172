from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class SourceEnum(enum.Enum):
    web = "web"
    mobile = "mobile"
    integration = "integration"
