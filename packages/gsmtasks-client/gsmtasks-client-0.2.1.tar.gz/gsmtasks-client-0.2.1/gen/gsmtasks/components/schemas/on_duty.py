from __future__ import annotations

import typing
import lapidary_base
import pydantic


class OnDuty(pydantic.BaseModel):
    account: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


OnDuty.update_forward_refs()
