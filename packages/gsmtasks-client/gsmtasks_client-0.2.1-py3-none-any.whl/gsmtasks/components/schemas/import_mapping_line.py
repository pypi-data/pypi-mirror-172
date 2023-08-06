from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent


class ImportMappingLine(pydantic.BaseModel):
    from_field: typing.Annotated[
        str,
        pydantic.Field(
            max_length=100,
        ),
    ]

    to_field: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    format: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=200,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


ImportMappingLine.update_forward_refs()
