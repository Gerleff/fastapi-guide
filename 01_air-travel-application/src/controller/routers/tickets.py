from fastapi import APIRouter, Depends
from starlette import status

router = APIRouter(prefix="/profile/trips", tags=["Tickets"])


@router.get("", response_model=list[TripForPassengerOutputSchema])
async def get_profile_trips(storage: Storage = Depends(get_example_storage)):
    return storage.pass_in_trip.filter()


@router.get("/{_id}", response_model=TripForPassengerOutputSchema)
async def get_profile_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    return storage.pass_in_trip.get_by_id(_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TripForPassengerOutputSchema,
)
async def add_profile_trip(
    pass_in_trip_data: TripForPassengerInputSchema, storage: Storage = Depends(get_example_storage)
):
    pass_in_trip_data_dict = pass_in_trip_data.dict()
    trip_id = pass_in_trip_data_dict.pop("trip")
    if not (trip := storage.trips.get_by_id(trip_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trip with that id does not exist")
    return storage.pass_in_trip.insert(TripForPassengerOutputSchema(trip=trip, **pass_in_trip_data_dict))


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_trip(_id: int, storage: Storage = Depends(get_example_storage)):
    storage.trips.delete_by_id(_id)
