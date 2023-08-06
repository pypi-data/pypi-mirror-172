from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent
import uuid


class Addon(pydantic.BaseModel):
    id: typing.Annotated[
        typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    name: typing.Annotated[
        str,
        pydantic.Field(
            max_length=100,
        ),
    ]

    short_description: typing.Annotated[str, pydantic.Field()]

    description: typing.Annotated[str, pydantic.Field()]

    price: typing.Annotated[
        str,
        pydantic.Field(
            max_length=50,
        ),
    ]

    unit: typing.Annotated[
        str,
        pydantic.Field(
            max_length=50,
        ),
    ]

    icon: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


Addon.update_forward_refs()
