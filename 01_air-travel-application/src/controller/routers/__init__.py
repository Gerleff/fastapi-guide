from .users.admin import router as admin_users_router
from .users.profile import router as profile_users_router
from .companies import router as companies_router
from .healthcheck import router as healthcheck_router
from .trips import router as trips_router
from .tickets.admin import router as admin_tickets_router
from .tickets.profile import router as profile_tickets_router

api_routers = (
    healthcheck_router,
    admin_users_router,
    profile_users_router,
    companies_router,
    trips_router,
    admin_tickets_router,
    profile_tickets_router,
)

__all__ = (api_routers,)
