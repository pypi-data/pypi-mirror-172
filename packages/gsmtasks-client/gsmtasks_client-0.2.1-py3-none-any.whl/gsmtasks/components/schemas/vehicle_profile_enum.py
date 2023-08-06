from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class VehicleProfileEnum(enum.Enum):
    bike = "bike"
    bus = "bus"
    car = "car"
    foot = "foot"
    scooter = "scooter"
    small_truck = "small_truck"
    truck = "truck"
