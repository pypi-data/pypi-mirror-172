from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class BillingStripePaymentsListFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class BillingStripePaymentsListState(enum.Enum):
    draft = "draft"
    failed = "failed"
    saved = "saved"
    settled = "settled"
    rejected = "rejected"
    retried = "retried"
    cancelled = "cancelled"


class BillingStripePaymentsListStripeState(enum.Enum):
    none = None
    requires_payment_method = "requires_payment_method"
    requires_confirmation = "requires_confirmation"
    requires_capture = "requires_capture"
    requires_action = "requires_action"
    processing = "processing"
    succeeded = "succeeded"
    canceled = "canceled"


class BillingStripePaymentsList(pydantic.BaseModel):
    q_billable_account: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="billable_account",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_cursor: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="cursor",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_format: typing.Annotated[
        typing.Union[
            BillingStripePaymentsListFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_invoice: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="invoice",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_ordering: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="ordering",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_page_size: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="page_size",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_state: typing.Annotated[
        typing.Union[
            BillingStripePaymentsListState,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="state",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_stripe_state: typing.Annotated[
        typing.Union[
            BillingStripePaymentsListStripeState,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="stripe_state",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


BillingStripePaymentsList.update_forward_refs()
