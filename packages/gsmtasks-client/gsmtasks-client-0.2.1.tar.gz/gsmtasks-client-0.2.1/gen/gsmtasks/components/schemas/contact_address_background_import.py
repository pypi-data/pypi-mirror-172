from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.tasks_background_import_state_enum
import lapidary_base.absent
import uuid


class ContactAddressBackgroundImportContactAddressesDataItem(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class ContactAddressBackgroundImportErrors(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class ContactAddressBackgroundImport(pydantic.BaseModel):
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

    created_by: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    contact_addresses_data: typing.Annotated[
        typing.Union[
            list[
                ContactAddressBackgroundImportContactAddressesDataItem,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.write,
        ),
    ] = lapidary_base.absent.ABSENT

    state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.tasks_background_import_state_enum.TasksBackgroundImportStateEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    started_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    completed_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    failed_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    errors: typing.Annotated[
        typing.Union[
            ContactAddressBackgroundImportErrors,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    celery_task_id: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    contact_addresses_created: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
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


ContactAddressBackgroundImportContactAddressesDataItem.update_forward_refs()
ContactAddressBackgroundImportErrors.update_forward_refs()
ContactAddressBackgroundImport.update_forward_refs()
