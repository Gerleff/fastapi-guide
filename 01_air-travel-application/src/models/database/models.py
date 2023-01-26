from datetime import datetime
from pydantic.dataclasses import dataclass

from models.enum import UserRoleEnum, PlaneEnum


@dataclass(kw_only=True)
class BaseDBModel:
    id: int | None = None  # Before storing in DB id = None

    class Meta:
        table = None


@dataclass
class TripModel(BaseDBModel):
    company: int
    plane: PlaneEnum
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime

    class Meta:
        table = "trips"


@dataclass
class CompanyModel(BaseDBModel):
    name: str

    class Meta:
        table = "companies"


@dataclass
class PassInTripModel(BaseDBModel):
    trip: int
    passenger: int
    place: str

    class Meta:
        table = "pass_in_trip"


@dataclass
class UserModel(BaseDBModel):
    name: str
    role: UserRoleEnum

    class Meta:
        table = "users"
