"""
Schemas are used to define and validate incoming and outgoing data, for which service is awared of.
Schemas are inpired by https://sql-academy.org/ru/trainer/tasks/9
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator, constr, root_validator, conint, Extra


class PlaneEnum(str, Enum):
    AIRBUS = "AirBus"
    BOEING = "Boeing"
    WONDER_PLANE = "WonderPlane"


# Input schemas.
class CompanyInputSchema(BaseModel):
    name: constr(min_length=1, max_length=64)

    class Config:
        """More https://docs.pydantic.dev/usage/model_config/"""

        extra = Extra.forbid


class TripInputSchema(BaseModel, extra=Extra.forbid):
    company: conint(gt=0)
    plane: PlaneEnum
    town_from: constr(min_length=1, max_length=64)
    town_to: constr(min_length=1, max_length=64)
    time_out: datetime
    time_in: datetime

    # Any error raised during validation normally will cause RequestValidationError end 422 Response with link to field
    @root_validator()
    def check_town_pre(cls, values: dict):
        assert values["town_to"] != values["town_from"], "Trips to the same town shouldn't be planned"
        return values

    @validator("time_in")
    def check_time(cls, value: datetime, values: dict):
        assert value > values["time_out"], "Time out must be lesser than time in"
        return value


class TripForPassengerInputSchema(BaseModel):
    place: constr(regex=r"^[A-F]\d\d$")
    trip: conint(gt=0)


# Output schemas. Also used to store in pythonic storage
class CompanyOutputSchema(BaseModel):
    id: int | None
    name: str


class TripOutputSchema(BaseModel):
    id: int | None
    company: CompanyOutputSchema
    plane: str
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime


class TripForPassengerOutputSchema(BaseModel):
    id: int | None
    place: str
    trip: TripOutputSchema
