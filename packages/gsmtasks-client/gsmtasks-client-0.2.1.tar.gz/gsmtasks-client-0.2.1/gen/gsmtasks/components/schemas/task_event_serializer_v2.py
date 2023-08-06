from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.blank_enum
import gsmtasks.components.schemas.event_enum
import gsmtasks.components.schemas.field_enum
import gsmtasks.components.schemas.location
import gsmtasks.components.schemas.task_event_task
import gsmtasks.components.schemas.task_event_transition_states_enum
import lapidary_base.absent
import uuid


class TaskEventSerializerV2(pydantic.BaseModel):
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

    task: typing.Annotated[
        gsmtasks.components.schemas.task_event_task.TaskEventTask, pydantic.Field()
    ]

    task_command: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    field: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.field_enum.FieldEnum,
            gsmtasks.components.schemas.blank_enum.BlankEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    event: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.event_enum.EventEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    from_state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.task_event_transition_states_enum.TaskEventTransitionStatesEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    to_state: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.task_event_transition_states_enum.TaskEventTransitionStatesEnum,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    user: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    notes: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    location: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.location.Location,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    assignee: typing.Annotated[str, pydantic.Field()]

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


TaskEventSerializerV2.update_forward_refs()
