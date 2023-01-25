from fastapi import APIRouter, Depends
from starlette import status

router = APIRouter(prefix="/trips", tags=["Trip"])


@router.get("", response_model=list[TripOutputSchema])
async def get_trips(plane: PlaneEnum | None = None, storage: Storage = Depends(get_example_storage)):
    return storage.trips.filter(plane=plane)


@router.get("/{_id}", response_model=TripOutputSchema, tags=["Trip"])
async def get_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    return storage.trips.get_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TripOutputSchema)
async def add_trip(trip_data: TripInputSchema, storage: Storage = Depends(get_example_storage)):
    trip_data_dict = trip_data.dict()
    company_id = trip_data_dict.pop("company")
    if not (company := storage.companies.get_by_id(company_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company with that id does not exist")
    return storage.trips.insert(TripOutputSchema(company=company, **trip_data_dict))


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    storage.trips.delete_by_id(_id)
