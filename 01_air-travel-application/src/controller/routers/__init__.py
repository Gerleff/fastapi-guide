# from .users import router as users_router
from .companies import router as companies_router
from .healthcheck import router as healthcheck_router
from .trips import router as trips_router

# from .tickets import router as tickets_router

api_routers = (
    healthcheck_router,
    # users_router,
    companies_router,
    trips_router,
    # tickets_router
)

__all__ = (api_routers,)
