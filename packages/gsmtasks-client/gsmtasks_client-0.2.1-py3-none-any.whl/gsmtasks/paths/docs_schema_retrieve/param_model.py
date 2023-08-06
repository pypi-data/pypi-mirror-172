from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum
import lapidary_base.absent


class DocsSchemaRetrieveFormat(enum.Enum):
    json = "json"
    yaml = "yaml"


class DocsSchemaRetrieveLang(enum.Enum):
    de = "de"
    en = "en"
    es = "es"
    et = "et"
    fi = "fi"
    fr = "fr"
    it = "it"
    lt = "lt"
    lv = "lv"
    pl = "pl"
    ru = "ru"
    sv = "sv"


class DocsSchemaRetrieve(pydantic.BaseModel):
    q_format: typing.Annotated[
        typing.Union[
            DocsSchemaRetrieveFormat,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="format",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    q_lang: typing.Annotated[
        typing.Union[
            DocsSchemaRetrieveLang,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(
            alias="lang",
            in_=lapidary_base.ParamPlacement.query,
        ),
    ] = lapidary_base.absent.ABSENT

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True


DocsSchemaRetrieve.update_forward_refs()
