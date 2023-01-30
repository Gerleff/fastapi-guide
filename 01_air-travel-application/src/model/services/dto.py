from pydantic import BaseModel, Extra

from model.db_entities.models import CompanyModel, TripModel, UserModel, PassInTripModel


class BaseDTO(BaseModel, orm_mode=True, extra=Extra.allow):
    @classmethod
    def from_database(cls, *args, **kwargs) -> "BaseDTO":
        raise NotImplementedError


class CompanyDTO(BaseDTO):
    @classmethod
    def from_database(cls, company: CompanyModel) -> "CompanyDTO":
        return cls.parse_obj(company)


class TripDTO(BaseDTO):
    company: int | CompanyDTO

    @classmethod
    def from_database(cls, trip: TripModel, company: CompanyModel) -> "TripDTO":
        dto = cls.parse_obj(trip)
        dto.company = company
        return dto


class UserDTO(BaseDTO):
    @classmethod
    def from_database(cls, user: UserModel) -> "UserDTO":
        return cls.parse_obj(user)


class TicketDTO(BaseDTO):
    trip: int | TripDTO
    passenger: int | UserDTO | None

    @classmethod
    def from_database(
        cls, ticket: PassInTripModel, trip: TripModel, company: CompanyModel, user: UserModel | None = None
    ) -> "TicketDTO":
        trip_dto = TripDTO.from_database(trip, company)
        dto = cls.parse_obj(ticket)
        dto.trip = trip_dto
        if user:
            dto.passenger = UserDTO.from_database(user)
        return dto
