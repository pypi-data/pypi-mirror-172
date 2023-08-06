from __future__ import annotations

import typing
import lapidary_base
import pydantic


class ConfigurationSettingsTaskCommandQueueLimit(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class ConfigurationSettings(pydantic.BaseModel):
    task_command_queue_limit: typing.Annotated[
        ConfigurationSettingsTaskCommandQueueLimit, pydantic.Field()
    ]

    date_format: typing.Annotated[str, pydantic.Field()]

    time_format: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


ConfigurationSettingsTaskCommandQueueLimit.update_forward_refs()
ConfigurationSettings.update_forward_refs()
