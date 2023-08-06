from __future__ import annotations

import typing
import lapidary_base
import pydantic
import gsmtasks.components.schemas.level_enum
import lapidary_base.absent


class ConfigurationNotification(pydantic.BaseModel):
    level: typing.Annotated[
        gsmtasks.components.schemas.level_enum.LevelEnum, pydantic.Field()
    ]

    message: typing.Annotated[str, pydantic.Field()]

    url: typing.Annotated[
        typing.Union[
            str,
            None,
        ],
        pydantic.Field(),
    ]

    persist: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    open_in_new_window: typing.Annotated[
        typing.Union[
            bool,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


ConfigurationNotification.update_forward_refs()
