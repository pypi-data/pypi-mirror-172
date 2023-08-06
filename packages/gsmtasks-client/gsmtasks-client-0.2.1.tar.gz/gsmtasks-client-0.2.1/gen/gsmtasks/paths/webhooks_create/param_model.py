from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class WebhooksCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class WebhooksCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            WebhooksCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


WebhooksCreate.update_forward_refs()
