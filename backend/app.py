from http import HTTPStatus
from typing import Any, Sequence

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from datamodels import Query
from spotify import Spotify

app = FastAPI()
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


@app.post("/api/getTracks/")
def get_top(query: Query):
    spotify = Spotify(query.accessToken)

    # Get recent 20 songs
    res = spotify.get_saved_tracks()

    ids = []
    for item in res.json()["items"]:
        ids.append(item["track"]["id"])

    # Get audio features
    audio_features = spotify.get_audio_features(",".join(ids)).json()

    # Mean of audio features
    df = pd.DataFrame(audio_features["audio_features"])
    selected_columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    means = df[selected_columns].mean()

    return means.to_dict()
