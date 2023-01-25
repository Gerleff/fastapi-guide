from models.database.models import TripModel, CompanyModel
from models.schemas.input import TripInputSchema, CompanyInputSchema
from models.schemas.output import TripOutputSchema, CompanyOutputSchema


class CompanySerializer:
    def serialize(self, model: CompanyModel) -> CompanyOutputSchema:
        return CompanyOutputSchema(**model.__dict__)

    def deserialize(self, schema: CompanyInputSchema) -> CompanyModel:
        return CompanyModel(**schema.dict())


class TripSerializer:
    def serialize(self, model: TripModel) -> TripOutputSchema:
        ...

    def deserialize(self, schema: TripInputSchema) -> TripModel:
        ...
