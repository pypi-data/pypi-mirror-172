from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent
import uuid


class TaskAddressFeaturesRetrieveFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class TaskAddressFeaturesRetrieve(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            TaskAddressFeaturesRetrieveFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    p_id: typing.Annotated[
        uuid.UUID,
        pydantic.Field(
            alias="id",
            in_=lapidary_base.ParamPlacement.path,
        ),
    ]

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


TaskAddressFeaturesRetrieve.update_forward_refs()
