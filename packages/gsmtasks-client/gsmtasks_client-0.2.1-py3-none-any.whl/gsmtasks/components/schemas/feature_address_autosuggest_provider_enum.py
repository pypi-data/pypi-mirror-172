from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class FeatureAddressAutosuggestProviderEnum(enum.Enum):
    google = "google"
    heremaps = "heremaps"
    regio = "regio"
    janaseta = "janaseta"
