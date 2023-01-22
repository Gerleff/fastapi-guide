from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from starlette import status
from starlette.requests import Request

from settings import settings
from storage import Storage
from schemas import (
    CompanyOutputSchema,
    TripOutputSchema,
    TripForPassengerOutputSchema,
    CompanyInputSchema,
    TripInputSchema,
    TripForPassengerInputSchema,
    PlaneEnum,
)

app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])


@app.on_event("startup")
def init_simple_storage():
    app.state.storage = Storage.parse_file("storage.json")


@app.on_event("shutdown")
def save_simple_storage():
    with open("storage.json", "w") as file:
        file.write(app.state.storage.json(indent=4, ensure_ascii=False))


def get_example_storage(request: Request) -> Storage:
    return request.app.state.storage


# For PATCH endpoints it is required to define separated schemas with "type | None" type-hint
# Companies
@app.get("/companies", response_model=list[CompanyOutputSchema], tags=["Company"])
async def get_companies(storage: Storage = Depends(get_example_storage)):
    return storage.companies.filter()


@app.get("/companies/{_id}", response_model=CompanyOutputSchema, tags=["Company"])
async def get_company(_id: int, storage: Storage = Depends(get_example_storage)):
    return storage.companies.get_by_id(_id)


@app.post("/companies", status_code=status.HTTP_201_CREATED, response_model=CompanyOutputSchema, tags=["Company"])
async def add_company(company_data: CompanyInputSchema, storage: Storage = Depends(get_example_storage)):
    return storage.companies.insert(CompanyOutputSchema(**company_data.dict()))


@app.delete("/companies/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Company"])
async def delete_company(_id: int, storage: Storage = Depends(get_example_storage)):
    storage.companies.delete_by_id(_id)


# Trips
@app.get("/trips", response_model=list[TripOutputSchema], tags=["Trip"])
async def get_trips(plane: PlaneEnum | None = None, storage: Storage = Depends(get_example_storage)):
    return storage.trips.filter(plane=plane)


@app.get("/trips/{_id}", response_model=TripOutputSchema, tags=["Trip"])
async def get_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    return storage.trips.get_by_id(_id)


@app.post("/trips", status_code=status.HTTP_201_CREATED, response_model=TripOutputSchema, tags=["Trip"])
async def add_trip(trip_data: TripInputSchema, storage: Storage = Depends(get_example_storage)):
    trip_data_dict = trip_data.dict()
    company_id = trip_data_dict.pop("company")
    if not (company := storage.companies.get_by_id(company_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company with that id does not exist")
    return storage.trips.insert(TripOutputSchema(company=company, **trip_data_dict))


@app.delete("/trips/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Trip"])
async def delete_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    storage.trips.delete_by_id(_id)


# Profile Trip
@app.get("/profile/trips", response_model=list[TripForPassengerOutputSchema], tags=["Profile Trip"])
async def get_profile_trips(storage: Storage = Depends(get_example_storage)):
    return storage.pass_in_trip.filter()


@app.get("/profile/trips/{_id}", response_model=TripForPassengerOutputSchema, tags=["Profile Trip"])
async def get_profile_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    return storage.pass_in_trip.get_by_id(_id)


@app.post(
    "/profile/trips",
    status_code=status.HTTP_201_CREATED,
    response_model=TripForPassengerOutputSchema,
    tags=["Profile Trip"],
)
async def add_profile_trip(
    pass_in_trip_data: TripForPassengerInputSchema, storage: Storage = Depends(get_example_storage)
):
    pass_in_trip_data_dict = pass_in_trip_data.dict()
    trip_id = pass_in_trip_data_dict.pop("trip")
    if not (trip := storage.trips.get_by_id(trip_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trip with that id does not exist")
    return storage.pass_in_trip.insert(TripForPassengerOutputSchema(trip=trip, **pass_in_trip_data_dict))


@app.delete("/profile/trips/{_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Profile Trip"])
async def delete_profile_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    storage.trips.delete_by_id(_id)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=settings.HOST, port=settings.PORT, reload=True)
