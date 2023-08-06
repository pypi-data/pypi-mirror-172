from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class AppEnum(enum.Enum):
    android = "android"
    ios = "ios"
    web = "web"
