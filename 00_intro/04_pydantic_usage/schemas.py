from datetime import datetime
from pydantic import BaseModel, validator, constr, root_validator, conint


# Input
class CompanyInputSchema(BaseModel):
    name: constr(min_length=1, max_length=64)


class TripInputSchema(BaseModel):
    company: conint(gt=0)
    plane: constr(min_length=1, max_length=64)
    town_from: constr(min_length=1, max_length=64)
    town_to: constr(min_length=1, max_length=64)
    time_out: datetime
    time_in: datetime

    @root_validator(pre=True)
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


# Output
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
