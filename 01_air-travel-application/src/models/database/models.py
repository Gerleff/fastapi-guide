from datetime import datetime
from pydantic.dataclasses import dataclass

from models.enum import UserRoleEnum, PlaneEnum


@dataclass
class TripModel:
    id: int
    company: int
    plane: PlaneEnum
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime

    class Meta:
        table = "trips"


@dataclass
class CompanyModel:
    id: int
    name: str

    class Meta:
        table = "companies"


@dataclass
class PassInTripModel:
    id: int
    trip: int
    passenger: int
    place: str

    class Meta:
        table = "pass_in_trip"


@dataclass
class UserModel:
    id: int
    name: str
    role: UserRoleEnum

    class Meta:
        table = "users"
