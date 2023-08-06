from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class TaskImportCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class TaskImportCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            TaskImportCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


TaskImportCreate.update_forward_refs()
