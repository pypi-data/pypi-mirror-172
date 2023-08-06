from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import lapidary_base.absent
import uuid


class InvoiceItem(pydantic.BaseModel):
    id: typing.Annotated[
        typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    invoice: typing.Annotated[str, pydantic.Field()]

    name: typing.Annotated[
        str,
        pydantic.Field(
            max_length=200,
        ),
    ]

    unit_price: typing.Annotated[
        str,
        pydantic.Field(
            regex=r"^-?\d{0,7}(?:\.\d{0,2})?$",
        ),
    ]

    quantity: typing.Annotated[
        str,
        pydantic.Field(
            regex=r"^-?\d{0,7}(?:\.\d{0,4})?$",
        ),
    ]

    unit: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=50,
        ),
    ] = lapidary_base.absent.ABSENT

    total: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
            regex=r"^-?\d{0,7}(?:\.\d{0,2})?$",
        ),
    ] = lapidary_base.absent.ABSENT

    created_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    updated_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


InvoiceItem.update_forward_refs()
