import random
from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings, validator, constr, root_validator, Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Iterator
import uvicorn
from starlette import status


# Input
class CompanyInputSchema(BaseModel):
    name: str


class TripInputSchema(BaseModel):
    company: int
    plane: str
    town_from: str
    town_to: str
    time_out: datetime
    time_in: datetime

    @root_validator(pre=True)
    def check_town_pre(cls, values: dict):
        assert values["town_to"] != values["town_from"], "Trips to the same town shouldn't be planned"
        return values

    @root_validator()
    def check_town(cls, values: "TripInputSchema"):
        assert values.town_to != values.town_from, "Trips to the same town shouldn't be planned"
        return values

    @validator("time_in")
    def check_time(cls, value: datetime, values: dict):
        try:
            assert value > values["time_out"], "Time out must be lesser than time in"
        except AssertionError:
            return value + timedelta(hours=random.randint(1, 10))
        return value

    @validator("company")
    def company_fk_check(cls, value: int):
        assert storage.companies.get_by_id(value), "Company with that id does not exist"
        return value


class TripForPassengerInputSchema(BaseModel):
    place: constr(regex=r"^[A-F]\d\d$")
    trip: int

    @validator("trip")
    def trip_fk_check(cls, value: int):
        assert storage.trips.get_by_id(value), "Trip with that id does not exist"
        return value


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


# pythonic storage =)
SchemaToStoreVar = TypeVar("SchemaToStoreVar", bound=BaseModel)


class GenericStorageList(GenericModel, Generic[SchemaToStoreVar]):
    __root__: list[SchemaToStoreVar] = Field(default_factory=list)

    # ToDO validate each __root__ elem

    def __iter__(self) -> Iterator[SchemaToStoreVar]:
        return self.__root__.__iter__()

    def filter(self):
        return self.__root__

    def get_by_id(self, _id: int) -> SchemaToStoreVar:
        for elem in self:
            if elem.id == _id:
                return elem

    def insert(self, value: SchemaToStoreVar) -> SchemaToStoreVar:
        if self.__root__:
            assert isinstance(value, type(_last_elem := self.__root__[-1])), "Entities in storage must be the same type"
            value.id = _last_elem.id + 1
        else:
            value.id = 1
        self.__root__.append(value)
        return value

    def delete_by_id(self, _id: int):
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                del self.__root__[elem_index]


class Storage(BaseModel):
    companies: GenericStorageList[CompanyOutputSchema]
    trips: GenericStorageList[TripOutputSchema]
    pass_in_trip: GenericStorageList[TripForPassengerOutputSchema]


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

storage = Storage(
    companies=[_company := CompanyOutputSchema(id=1, name="AirWonder")],
    trips=[
        _trip := TripOutputSchema(
            id=1,
            company=_company,
            plane="WonderPlane",
            town_from="Dubai",
            town_to="Saratov",
            time_out=datetime.now(),
            time_in=datetime.now() + timedelta(hours=3),
        )
    ],
    pass_in_trip=[TripForPassengerOutputSchema(id=1, trip=_trip, place="A21")],
)

app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])


# Companies
@app.get("/companies", response_model=list[CompanyOutputSchema], tags=["Company"])
async def get_companies():
    return storage.companies.filter()


@app.get("/companies/{_id}", response_model=CompanyOutputSchema, tags=["Company"])
async def get_company(_id: int):
    return storage.companies.get_by_id(_id)


@app.post("/companies", status_code=status.HTTP_201_CREATED, response_model=CompanyOutputSchema, tags=["Company"])
async def add_company(company_data: CompanyInputSchema):
    return storage.companies.insert(CompanyOutputSchema(**company_data.dict()))


@app.delete("/companies/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Company"])
async def delete_company(_id: int):
    storage.companies.delete_by_id(_id)


# Trips
@app.get("/trips", response_model=list[TripOutputSchema], tags=["Trip"])
async def get_trips():
    return storage.trips.filter()


@app.get("/trips/{_id}", response_model=TripOutputSchema, tags=["Trip"])
async def get_trip(_id: int):
    return storage.trips.get_by_id(_id)


@app.post("/trips", status_code=status.HTTP_201_CREATED, response_model=TripOutputSchema, tags=["Trip"])
async def add_trip(trip_data: TripInputSchema):
    trip_data_dict = trip_data.dict()
    company_id = trip_data_dict.pop("company")
    return storage.trips.insert(TripOutputSchema(company=storage.companies.get_by_id(company_id), **trip_data_dict))


@app.delete("/trips/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Trip"])
async def delete_trip(_id: int):
    storage.trips.delete_by_id(_id)


# Profile Trip
@app.get("/profile/trips", response_model=list[TripForPassengerOutputSchema], tags=["Profile Trip"])
async def get_profile_trips():
    return storage.pass_in_trip.filter()


@app.get("/profile/trips/{_id}", response_model=TripForPassengerOutputSchema, tags=["Profile Trip"])
async def get_profile_trip(_id: int):
    return storage.pass_in_trip.get_by_id(_id)


@app.post(
    "/profile/trips",
    status_code=status.HTTP_201_CREATED,
    response_model=TripForPassengerOutputSchema,
    tags=["Profile Trip"],
)
async def add_profile_trip(pass_in_trip_data: TripForPassengerInputSchema):
    pass_in_trip_data_dict = pass_in_trip_data.dict()
    trip_id = pass_in_trip_data_dict.pop("trip")
    return storage.pass_in_trip.insert(
        TripForPassengerOutputSchema(trip=storage.trips.get_by_id(trip_id), **pass_in_trip_data_dict)
    )


@app.delete("/profile/trips/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Profile Trip"])
async def delete_profile_trip(_id: int):
    storage.trips.delete_by_id(_id)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=settings.HOST, port=settings.PORT, reload=True)
