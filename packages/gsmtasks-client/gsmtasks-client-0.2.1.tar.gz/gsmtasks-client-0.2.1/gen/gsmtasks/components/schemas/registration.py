from __future__ import annotations

import typing
import lapidary_base
import pydantic
import gsmtasks.components.schemas.registration_account
import gsmtasks.components.schemas.registration_user
import lapidary_base.absent


class Registration(pydantic.BaseModel):
    account: typing.Annotated[
        gsmtasks.components.schemas.registration_account.RegistrationAccount,
        pydantic.Field(),
    ]

    user: typing.Annotated[
        gsmtasks.components.schemas.registration_user.RegistrationUser, pydantic.Field()
    ]

    token: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


Registration.update_forward_refs()
