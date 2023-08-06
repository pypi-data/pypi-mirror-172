from __future__ import annotations

import typing
import lapidary_base
import pydantic
import datetime
import gsmtasks.components.schemas.nested_address
import lapidary_base.absent


class TaskCommandTaskDataMetafields(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class TaskCommandTaskData(pydantic.BaseModel):
    scheduled_time: typing.Annotated[
        typing.Union[
            datetime.datetime,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    position: typing.Annotated[
        typing.Union[
            float,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            ge=0.0,
            le=253402300799.0,
        ),
    ] = lapidary_base.absent.ABSENT

    metafields: typing.Annotated[
        typing.Union[
            TaskCommandTaskDataMetafields,
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

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


TaskCommandTaskDataMetafields.update_forward_refs()
TaskCommandTaskData.update_forward_refs()
