from __future__ import annotations

import typing
import lapidary_base
import pydantic
import uuid


class RecurrencesRetrieve(pydantic.BaseModel):
    p_id: typing.Annotated[
        uuid.UUID,
        pydantic.Field(
            alias="id",
            in_=lapidary_base.ParamPlacement.path,
        ),
    ]

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


RecurrencesRetrieve.update_forward_refs()
