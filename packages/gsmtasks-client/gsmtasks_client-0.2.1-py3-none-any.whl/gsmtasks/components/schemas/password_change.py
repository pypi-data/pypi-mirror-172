from __future__ import annotations

import typing
import lapidary_base
import pydantic


class PasswordChange(pydantic.BaseModel):
    old_password: typing.Annotated[str, pydantic.Field()]

    new_password1: typing.Annotated[str, pydantic.Field()]

    new_password2: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


PasswordChange.update_forward_refs()
