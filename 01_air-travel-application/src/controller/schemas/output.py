from datetime import datetime

from pydantic import BaseModel

from model.enum import UserRoleEnum


class CompanyOutputSchema(BaseModel):
    id: int
    name: str


class TripOutputSchema(BaseModel):
    id: int
    company: CompanyOutputSchema
    plane: str
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime


class UserProfileOutputSchema(BaseModel):
    role: UserRoleEnum
    name: str


class UserAdminOutputSchema(BaseModel):
    id: int
    role: UserRoleEnum
    name: str


class TicketProfileOutputSchema(BaseModel):
    id: int
    place: str
    trip: TripOutputSchema


class TicketAdminOutputSchema(BaseModel):
    id: int
    place: str
    trip: TripOutputSchema
    passenger: UserAdminOutputSchema
