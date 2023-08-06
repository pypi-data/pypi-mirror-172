from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent
import uuid


class AccountRoleToken(pydantic.BaseModel):
    token: typing.Annotated[
        typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


AccountRoleToken.update_forward_refs()
