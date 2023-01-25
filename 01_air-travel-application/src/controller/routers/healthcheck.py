from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@router.get("/ping")
async def healthcheck():
    return "pong"
