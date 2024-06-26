from http import HTTPStatus
from typing import Any, Sequence

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import Database
from datamodels import Query

app = FastAPI()
database = Database()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Custom exception handler for handling FastAPI RequestValidationErrors.

    Pydantic models throw RequestValidationErrors when validation errors occur.

    Args:
        _: FastAPI Request object (unused).
        exc (RequestValidationError): The raised RequestValidationError.

    Returns:
        JSONResponse: A JSON response containing information about the validation errors.
    """
    errors: Sequence[dict[str, Any]] = exc.errors()

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "message": f"An error occurred: {exc.__class__.__name__}",
                "details": [
                    {
                        "loc": ".".join(map(str, error.get("loc") or [])),
                        "error": error.get("msg"),
                    }
                    for error in errors
                ],
            }
        ),
    )


@app.post("/api/token/")
def get_token(query: Query):
    with open(".spotify_cached_token", "w") as f:
        f.write(query.accessToken)
