import random
from contextlib import suppress
from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings, validator, constr
from pydantic_factories import ModelFactory
import uvicorn


class DatabaseModels:
    """Taken from https://sql-academy.org/ru/trainer/tasks/9"""

    class TripModel(BaseModel):
        id: int
        company: int
        plane: str
        town_from: str
        town_to: str
        time_out: datetime
        time_in: datetime

        @validator("town_to")
        def check_town(cls, value: str, values: dict):
            assert value != values["town_from"], "Trips to the same town shouldn't be planned"
            return value

        @validator("time_in")
        def check_time(cls, value: datetime, values: dict):
            try:
                assert value > values["time_out"], "Time out must be lesser than time in"
            except AssertionError:
                return value + timedelta(hours=random.randint(1, 10))
            return value

    class CompanyModel(BaseModel):
        id: int
        name: str

    class PassInTripModel(BaseModel):
        id: int
        trip: int
        passenger: int
        place: constr(regex=r"^[A-F]\d\d$")

    class PassengerModel(BaseModel):
        id: int
        name: str


class Storage(BaseModel):
    companies: list[DatabaseModels.CompanyModel]
    passengers: list[DatabaseModels.PassengerModel]
    trips: list[DatabaseModels.TripModel]
    pass_in_trip: list[DatabaseModels.PassInTripModel]

    def get_by_id(self, attr: str, _id: int):
        # ToDo check attr
        for model in getattr(self, attr):
            if model.id == _id:
                return model
        return 404  # ToDo raise


class DatabaseFactories:
    # Used https://pypi.org/project/pydantic-factories/
    class TripFactory(ModelFactory):
        __model__ = DatabaseModels.TripModel

    class CompanyFactory(ModelFactory):
        __model__ = DatabaseModels.CompanyModel

    class PassInTripFactory(ModelFactory):
        __model__ = DatabaseModels.PassInTripModel

    class PassengerFactory(ModelFactory):
        __model__ = DatabaseModels.PassengerModel

    storage: Storage

    @classmethod
    def fill_storage(
        cls,
        passengers_count: int = 1,
        tickets_by_passenger_count: int = 5,
        companies_count: int = 10,
        trips_count: int = 20,
    ):
        companies = [cls.CompanyFactory.build(id=_id) for _id in range(1, companies_count + 1)]
        trips = [
            cls.TripFactory.build(id=_id, company=random.randint(1, companies_count))
            for _id in range(1, trips_count + 1)
        ]
        passengers, pass_in_trip = [], []
        for passenger_id in range(1, passengers_count + 1):
            passengers.append(passenger := cls.PassengerFactory.build(id=passenger_id))
            for ticket_id in range((passenger_id - 1) * tickets_by_passenger_count + 1, tickets_by_passenger_count + 1):
                pass_in_trip.append(
                    cls.PassInTripFactory.build(passenger=passenger.id, trip=random.randint(1, trips_count))
                )

        cls.storage = Storage(companies=companies, passengers=passengers, trips=trips, pass_in_trip=pass_in_trip)


# class OutputSchemas:
class CompanySchema(BaseModel):
    id: int
    name: str


class TripSchema(BaseModel):
    id: int
    company: CompanySchema
    plane: str
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime


class TripForPassengerOutputSchema(BaseModel):
    id: int
    place: str
    detail: TripSchema


class Settings(BaseSettings):
    class Config(BaseSettings.Config):
        env_prefix = "APP_"

    HOST: str = "localhost"
    PORT: int = 8000
    ADDRESS: str | None = None

    @validator("ADDRESS")
    def check_app_address(cls, value: str | None, values: dict) -> str:
        return value or f"http://{values.get('HOST')}:{values.get('PORT')}"


settings = Settings()

app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])


@app.on_event("startup")
def fill_storage():
    success = False
    while not success:
        with suppress(ValueError):
            DatabaseFactories.fill_storage()
            success = True


@app.get("/companies", response_model=list[CompanySchema])
async def get_companies():
    return [CompanySchema(**model.dict()) for model in DatabaseFactories.storage.companies]


@app.get("/trips", response_model=list[TripSchema])
async def get_companies():
    return [
        TripSchema(
            company=DatabaseFactories.storage.get_by_id("companies", trip_model.company),
            **trip_model.dict(
                exclude={
                    "company",
                }
            ),
        )
        for trip_model in DatabaseFactories.storage.trips
    ]


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=settings.HOST, port=settings.PORT, reload=True)
