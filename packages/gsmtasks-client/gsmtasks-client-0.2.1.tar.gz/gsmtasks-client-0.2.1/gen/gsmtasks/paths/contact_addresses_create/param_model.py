from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class ContactAddressesCreateFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class ContactAddressesCreate(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            ContactAddressesCreateFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


ContactAddressesCreate.update_forward_refs()
