from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.account_role_state_enum
import gsmtasks.components.schemas.nested_address
import gsmtasks.components.schemas.vehicle_profile_enum
import lapidary_base.absent
import uuid


class AccountRole(pydantic.BaseModel):
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

    account: typing.Annotated[str, pydantic.Field()]

    user: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.account_role_state_enum.AccountRoleStateEnum,
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
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    display_name: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    phone: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=128,
        ),
    ] = lapidary_base.absent.ABSENT

    vehicle_registration_number: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=32,
        ),
    ] = lapidary_base.absent.ABSENT

    vehicle_profile: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.vehicle_profile_enum.VehicleProfileEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    vehicle_capacity: typing.Annotated[
        typing.Union[
            list[
                int,
            ],
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    vehicle_speed_factor: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            regex=r"^-?\d{0,1}(?:\.\d{0,1})?$",
        ),
    ] = lapidary_base.absent.ABSENT

    vehicle_service_time_factor: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            regex=r"^-?\d{0,1}(?:\.\d{0,1})?$",
        ),
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

    signature_image: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    is_manager: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    is_worker: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    is_integration: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    is_active: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    is_on_duty: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    show_unassigned: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    last_time_location: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    activated_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    deleted_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
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


AccountRole.update_forward_refs()
