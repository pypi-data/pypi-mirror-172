from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class PasswordChangeCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class PasswordChangeCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            PasswordChangeCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


PasswordChangeCreate.update_forward_refs()
