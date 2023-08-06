from __future__ import annotations

import typing
import lapidary_base
import pydantic


class ConfigurationDefaultsTaskDuration(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


class ConfigurationDefaults(pydantic.BaseModel):
    task_duration: typing.Annotated[ConfigurationDefaultsTaskDuration, pydantic.Field()]

    distance_units: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


ConfigurationDefaultsTaskDuration.update_forward_refs()
ConfigurationDefaults.update_forward_refs()
