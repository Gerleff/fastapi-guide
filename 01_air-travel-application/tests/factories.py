import random

from pydantic_factories import ModelFactory

from sample import DatabaseModels, Storage


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
