from __future__ import annotations

import typing
import lapidary_base
import pydantic
import lapidary_base.absent


class TasksStatesCountResponseDates(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class TasksStatesCountResponse(pydantic.BaseModel):
    dates: typing.Annotated[
        typing.Union[
            TasksStatesCountResponseDates,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            direction=lapidary_base.ParamDirection.read,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


TasksStatesCountResponseDates.update_forward_refs()
TasksStatesCountResponse.update_forward_refs()
