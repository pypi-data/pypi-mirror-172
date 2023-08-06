from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class SignaturesCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class SignaturesCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            SignaturesCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


SignaturesCreate.update_forward_refs()
