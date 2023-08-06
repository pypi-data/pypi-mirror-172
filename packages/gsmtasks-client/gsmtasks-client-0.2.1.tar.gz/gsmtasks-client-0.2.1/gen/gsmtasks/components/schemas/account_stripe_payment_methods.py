from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent


class AccountStripePaymentMethods(pydantic.BaseModel):
    default_payment_method_id: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


AccountStripePaymentMethods.update_forward_refs()
