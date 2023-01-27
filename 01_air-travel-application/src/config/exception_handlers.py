from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from model.storage.exceptions import EntityNotFoundError


def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> Response:
    return JSONResponse({"detail": exc.message}, status_code=status.HTTP_404_NOT_FOUND)


exception_handlers = ((EntityNotFoundError, entity_not_found_handler),)
