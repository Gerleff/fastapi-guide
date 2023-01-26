from datetime import datetime

from pydantic import BaseModel

from models.enum import UserRoleEnum, PlaneEnum


class BaseDBModel(BaseModel):
    id: int | None = None  # Before storing in DB id = None

    class Meta:
        table = None


class TripModel(BaseDBModel):
    company: int
    plane: PlaneEnum
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime

    class Meta:
        table = "trips"


class CompanyModel(BaseDBModel):
    name: str

    class Meta:
        table = "companies"


class PassInTripModel(BaseDBModel):
    trip: int
    passenger: int
    place: str

    class Meta:
        table = "pass_in_trip"


class UserModel(BaseDBModel):
    name: str
    role: UserRoleEnum

    class Meta:
        table = "users"
