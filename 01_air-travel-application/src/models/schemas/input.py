from datetime import datetime

from pydantic import BaseModel, constr, conint, validator

from .utils import make_update_schema
from ..enum import PlaneEnum


class CompanyInputSchema(BaseModel):
    name: constr(min_length=1, max_length=64)


class TripInputSchema(BaseModel):
    company: conint(gt=0)
    plane: PlaneEnum
    town_from: constr(min_length=1, max_length=64)
    town_to: constr(min_length=1, max_length=64)
    time_out: datetime
    time_in: datetime

    @validator("town_to")
    def check_town_pre(cls, value: str, values: dict):
        assert value != values["town_from"], "Trips to the same town shouldn't be planned"
        return value

    @validator("time_in")
    def check_time(cls, value: datetime, values: dict):
        assert value > values["time_out"], "Time out must be lesser than time in"
        return value


class TicketInputSchema(BaseModel):
    place: constr(regex=r"^[A-F]\d\d$")
    trip: conint(gt=0)


CompanyUpdateSchema = make_update_schema(CompanyInputSchema)
TripUpdateSchema = make_update_schema(TripInputSchema)
TicketUpdateSchema = make_update_schema(TicketInputSchema)
