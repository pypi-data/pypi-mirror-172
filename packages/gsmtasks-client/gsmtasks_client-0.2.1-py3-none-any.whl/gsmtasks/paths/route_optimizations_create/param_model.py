from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class RouteOptimizationsCreateFormat(enum.Enum):
    json = "json"
    xml = "xml"


class RouteOptimizationsCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            RouteOptimizationsCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


RouteOptimizationsCreate.update_forward_refs()
