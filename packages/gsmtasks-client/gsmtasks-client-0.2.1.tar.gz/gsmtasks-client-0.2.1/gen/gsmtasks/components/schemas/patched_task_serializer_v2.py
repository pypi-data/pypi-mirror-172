from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.assignee_proximity_enum
import gsmtasks.components.schemas.nested_address
import gsmtasks.components.schemas.nested_contact
import gsmtasks.components.schemas.task_category_enum
import gsmtasks.components.schemas.task_state_enum
import lapidary_base.absent
import uuid


class PatchedTaskSerializerV2Duration(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedTaskSerializerV2Forms(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedTaskSerializerV2Metafields(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedTaskSerializerV2Counts(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedTaskSerializerV2Actions(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class PatchedTaskSerializerV2(pydantic.BaseModel):
    id: typing.Annotated[
        typing.Union[
            uuid.UUID,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    external_id: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    reference: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            max_length=100,
        ),
    ] = lapidary_base.absent.ABSENT

    barcodes: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
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

    account: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.task_state_enum.TaskStateEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    assignee: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    order: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    orderer: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.write,
        ),
    ] = lapidary_base.absent.ABSENT

    orderer_name: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    route: typing.Annotated[
        typing.Union[
            str,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    category: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.task_category_enum.TaskCategoryEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    contact: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.nested_contact.NestedContact,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    address: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.nested_address.NestedAddress,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    description: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    complete_after: typing.Annotated[
        typing.Union[
            datetime.datetime,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    complete_before: typing.Annotated[
        typing.Union[
            datetime.datetime,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    scheduled_time: typing.Annotated[
        typing.Union[
            datetime.datetime,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
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

    cancelled_at: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    auto_assign: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    assignee_proximity: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.assignee_proximity_enum.AssigneeProximityEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    position: typing.Annotated[
        typing.Union[
            float,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=0.0,
            le=253402300799.0,
        ),
    ] = lapidary_base.absent.ABSENT

    priority: typing.Annotated[
        typing.Union[
            int,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=-2147483648.0,
            le=2147483647.0,
        ),
    ] = lapidary_base.absent.ABSENT

    duration: typing.Annotated[
        typing.Union[
            PatchedTaskSerializerV2Duration,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    size: typing.Annotated[
        typing.Union[
            list[
                int,
            ],
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    forms: typing.Annotated[
        typing.Union[
            PatchedTaskSerializerV2Forms,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    documents: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    signatures: typing.Annotated[
        typing.Union[
            list[
                str,
            ],
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    metafields: typing.Annotated[
        typing.Union[
            PatchedTaskSerializerV2Metafields,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    trackers: typing.Annotated[
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

    issues: typing.Annotated[
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

    counts: typing.Annotated[
        typing.Union[
            PatchedTaskSerializerV2Counts,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    actions: typing.Annotated[
        typing.Union[
            PatchedTaskSerializerV2Actions,
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


PatchedTaskSerializerV2Duration.update_forward_refs()
PatchedTaskSerializerV2Forms.update_forward_refs()
PatchedTaskSerializerV2Metafields.update_forward_refs()
PatchedTaskSerializerV2Counts.update_forward_refs()
PatchedTaskSerializerV2Actions.update_forward_refs()
PatchedTaskSerializerV2.update_forward_refs()
