from datetime import datetime

from pydantic import BaseModel


class CompanyOutputSchema(BaseModel):
    name: str


class TripOutputSchema(BaseModel):
    company: CompanyOutputSchema
    plane: str
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime


class TicketOutputSchema(BaseModel):
    place: str
    trip: TripOutputSchema
