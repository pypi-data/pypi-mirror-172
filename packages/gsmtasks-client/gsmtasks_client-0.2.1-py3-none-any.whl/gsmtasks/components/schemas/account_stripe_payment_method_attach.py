from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent


class AccountStripePaymentMethodAttach(pydantic.BaseModel):
    stripe_customer_id: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=255,
        ),
    ] = lapidary_base.absent.ABSENT

    stripe_payment_method_id: typing.Annotated[
        str,
        pydantic.Field(
            max_length=255,
        ),
    ]

    set_default: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


AccountStripePaymentMethodAttach.update_forward_refs()
