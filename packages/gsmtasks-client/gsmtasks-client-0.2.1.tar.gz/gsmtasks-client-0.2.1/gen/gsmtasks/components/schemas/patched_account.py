from __future__ import annotations

import typing
import lapidary_base
import pydantic
import gsmtasks.components.schemas.account_billing_method_enum
import gsmtasks.components.schemas.account_state_enum
import gsmtasks.components.schemas.blank_enum
import gsmtasks.components.schemas.country_code_enum
import gsmtasks.components.schemas.date_format_enum
import gsmtasks.components.schemas.distance_units_enum
import gsmtasks.components.schemas.feature_address_autosuggest_provider_enum
import gsmtasks.components.schemas.language_enum
import gsmtasks.components.schemas.nested_address
import gsmtasks.components.schemas.objective_enum
import gsmtasks.components.schemas.task_expiry_state_enum
import gsmtasks.components.schemas.time_format_enum
import gsmtasks.components.schemas.timezone_enum
import gsmtasks.components.schemas.type21d_enum
import lapidary_base.absent
import uuid


class PatchedAccountTaskDuration(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedAccountTaskExpiryDurationFromCompleteAfter(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedAccountTaskExpiryDurationFromCompleteBefore(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedAccountAutoAssignRotate(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedAccount(pydantic.BaseModel):
    id: typing.Annotated[
        typing.Union[
            uuid.UUID,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    url: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    name: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.account_state_enum.AccountStateEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    type: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.type21d_enum.Type21dEnum,
            gsmtasks.components.schemas.blank_enum.BlankEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    slug: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
            regex=r"^[-a-zA-Z0-9_]+$",
        ),
    ] = lapidary_base.absent.ABSENT

    owner: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    email: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=254,
        ),
    ] = lapidary_base.absent.ABSENT

    notification_emails: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    review_emails: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    website: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=200,
        ),
    ] = lapidary_base.absent.ABSENT

    registry_code: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=20,
        ),
    ] = lapidary_base.absent.ABSENT

    vatin: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=20,
        ),
    ] = lapidary_base.absent.ABSENT

    language: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.language_enum.LanguageEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    timezone: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.timezone_enum.TimezoneEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    country_code: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.country_code_enum.CountryCodeEnum,
            gsmtasks.components.schemas.blank_enum.BlankEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    address: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.nested_address.NestedAddress,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    custom_integration_url: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    distance_units: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.distance_units_enum.DistanceUnitsEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    task_duration: typing.Annotated[
        typing.Union[
            PatchedAccountTaskDuration,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    task_expiry_duration_from_complete_after: typing.Annotated[
        typing.Union[
            PatchedAccountTaskExpiryDurationFromCompleteAfter,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    task_expiry_duration_from_complete_before: typing.Annotated[
        typing.Union[
            PatchedAccountTaskExpiryDurationFromCompleteBefore,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    task_expiry_state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.task_expiry_state_enum.TaskExpiryStateEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    assignee_proximity_radius: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=0.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    date_format: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.date_format_enum.DateFormatEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    time_format: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.time_format_enum.TimeFormatEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    route_start_address: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.nested_address.NestedAddress,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    route_end_address: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.nested_address.NestedAddress,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    optimize_after_create: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    optimization_objective: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.objective_enum.ObjectiveEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    reference_autogenerate: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    reference_offset: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=-2147483648.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    reference_prefix: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=50,
        ),
    ] = lapidary_base.absent.ABSENT

    reference_length: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=-2147483648.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    feature_show_unassigned_to_workers: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_task_created_sound: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_change_task_account: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    feature_show_tutorial: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_navigation_app_selection: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_navigation_use_address: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_task_accept: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_task_reject: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_app_task_search: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_address_autosuggest_provider: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.feature_address_autosuggest_provider_enum.FeatureAddressAutosuggestProviderEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_geocoding_country_code: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.country_code_enum.CountryCodeEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    feature_document_signing: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    feature_tracker_reviews_allowed: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    auto_assign_orders: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    auto_assign_max_tasks: typing.Annotated[
        typing.Union[
            int,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=-2147483648.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    auto_assign_max_distance: typing.Annotated[
        typing.Union[
            int,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=-2147483648.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    auto_assign_time_before: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    auto_assign_rotate: typing.Annotated[
        typing.Union[
            PatchedAccountAutoAssignRotate,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    auto_assign_optimize: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    dashboard_task_template: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    calendar_task_template: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    dashboard_worker_limit: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    managers: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    workers: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    stripe_customer_id: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    stripe_payment_method_id: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_method: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.account_billing_method_enum.AccountBillingMethodEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_name: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_company: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_address: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=200,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_country: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_email: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=254,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_phone: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=20,
        ),
    ] = lapidary_base.absent.ABSENT

    billing_vatin: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=20,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


PatchedAccountTaskDuration.update_forward_refs()
PatchedAccountTaskExpiryDurationFromCompleteAfter.update_forward_refs()
PatchedAccountTaskExpiryDurationFromCompleteBefore.update_forward_refs()
PatchedAccountAutoAssignRotate.update_forward_refs()
PatchedAccount.update_forward_refs()
