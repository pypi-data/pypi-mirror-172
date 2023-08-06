from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent
import uuid


class ReviewsRetrieveFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class ReviewsRetrieve(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            ReviewsRetrieveFormat,
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


ReviewsRetrieve.update_forward_refs()
