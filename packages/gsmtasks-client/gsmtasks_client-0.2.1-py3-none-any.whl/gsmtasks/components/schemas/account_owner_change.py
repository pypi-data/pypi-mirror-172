from __future__ import annotations

import typing
import lapidary_base
import pydantic


class AccountOwnerChange(pydantic.BaseModel):
    owner: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


AccountOwnerChange.update_forward_refs()
