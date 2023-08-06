from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.location
import lapidary_base.absent
import uuid


class Route(pydantic.BaseModel):
    id: typing.Annotated[
        typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    url: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    external_id: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    account: typing.Annotated[str, pydantic.Field()]

    code: typing.Annotated[
        str,
        pydantic.Field(
            max_length=100,
        ),
    ]

    description: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    assignee: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    start_time: typing.Annotated[
        typing.Union[
            datetime.datetime,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    start_location: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.location.Location,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    end_time: typing.Annotated[
        typing.Union[
            datetime.datetime,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    end_location: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.location.Location,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    created_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    updated_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


Route.update_forward_refs()
