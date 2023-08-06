from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class BillingTransactionsListFormat(enum.Enum):
    json = "json"
    xlsx = "xlsx"


class BillingTransactionsListState(enum.Enum):
    draft = "draft"
    failed = "failed"
    saved = "saved"
    settled = "settled"
    rejected = "rejected"
    voided = "voided"
    refunded = "refunded"
    retried = "retried"
    cancelled = "cancelled"
    imported = "imported"


class BillingTransactionsList(pydantic.BaseModel):
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

    q_customer: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="customer",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_format: typing.Annotated[
        typing.Union[
            BillingTransactionsListFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_invoice__account: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="invoice__account",
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
            BillingTransactionsListState,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="state",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


BillingTransactionsList.update_forward_refs()
