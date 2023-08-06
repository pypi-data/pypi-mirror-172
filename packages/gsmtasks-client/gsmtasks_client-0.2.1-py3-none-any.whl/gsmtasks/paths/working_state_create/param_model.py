from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class WorkingStateCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class WorkingStateCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            WorkingStateCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


WorkingStateCreate.update_forward_refs()
