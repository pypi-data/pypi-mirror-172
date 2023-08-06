from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class ModeEnum(enum.Enum):
    online = "online"
    offline = "offline"
