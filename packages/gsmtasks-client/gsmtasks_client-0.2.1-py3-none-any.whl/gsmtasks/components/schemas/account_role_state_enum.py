from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class AccountRoleStateEnum(enum.Enum):
    inactive = "inactive"
    active = "active"
    deleted = "deleted"
