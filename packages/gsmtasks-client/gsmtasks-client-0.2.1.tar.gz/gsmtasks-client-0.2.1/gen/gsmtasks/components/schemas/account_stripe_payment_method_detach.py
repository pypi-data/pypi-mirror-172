from __future__ import annotations

import typing
import lapidary_base
import pydantic


class AccountStripePaymentMethodDetach(pydantic.BaseModel):
    stripe_payment_method_id: typing.Annotated[
        str,
        pydantic.Field(
            max_length=255,
        ),
    ]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


AccountStripePaymentMethodDetach.update_forward_refs()
