from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class TrackersCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class TrackersCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            TrackersCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


TrackersCreate.update_forward_refs()
