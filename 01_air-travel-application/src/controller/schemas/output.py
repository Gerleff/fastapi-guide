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


class TicketOutputSchema(BaseModel):
    id: int
    place: str
    trip: TripOutputSchema


class UserOutputSchema(BaseModel):
    id: int
    role: UserRoleEnum
    name: str
