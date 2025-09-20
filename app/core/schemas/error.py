from typing import Annotated

from core.schemas.base import BaseSchema, NonEmptyString
from pydantic import Field
from starlette import status


class HTTPError(BaseSchema):
    detail: Annotated[NonEmptyString, Field(examples=["Service error"])]


def error_response(status_code: int) -> dict[int, dict[str, type[HTTPError]]]:
    return {
        status_code: {
            "model": HTTPError,
        }
    }


bad_request = error_response(status.HTTP_400_BAD_REQUEST)
unauthorized = error_response(status.HTTP_401_UNAUTHORIZED)
forbidden = error_response(status.HTTP_403_FORBIDDEN)
not_found = error_response(status.HTTP_404_NOT_FOUND)
conflict = error_response(status.HTTP_409_CONFLICT)

internal_server_error = error_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
