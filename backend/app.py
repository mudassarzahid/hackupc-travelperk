from http import HTTPStatus
from typing import Any, Sequence

import pandas as pd
import psycopg2
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import Database
from datamodels import Query
from spotify import Spotify

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


@app.post("/api/loadUserData/")
def get_top(query: Query):
    spotify = Spotify(query.accessToken)

    # Get recent 20 songs
    res = spotify.get_saved_tracks()

    ids = []
    for item in res.json()["items"]:
        ids.append(item["track"]["id"])

    # Get audio features
    audio_features = spotify.get_audio_features(",".join(ids)).json()
    user_data = spotify.get_user_data().json()

    # Mean of audio features
    df = pd.DataFrame(audio_features["audio_features"])
    selected_columns = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
    ]
    means = df[selected_columns].mean()
    cols = str(tuple(["spotify_uri"] + selected_columns)).replace("'", "")
    row = [user_data["uri"]] + list(means.to_dict().values())

    insert_stmt = (
        f"INSERT INTO user_data {cols} VALUES {tuple(row)} "
        f"ON CONFLICT (spotify_uri) DO UPDATE SET "
        f"{', '.join([f'{col}=EXCLUDED.{col}' for col in selected_columns])} RETURNING 1;"
    )
    database.execute_query(insert_stmt)

    return {
        "spotifyUri": user_data["uri"],
        "displayName": user_data["display_name"]
    }


@app.post("/api/findTravelBuddies/")
def get_top(query: Query):
    truncate_stmt = "TRUNCATE current_matches;"
    database.execute_dml_query(truncate_stmt)

    user_stmt = f"SELECT * FROM user_data WHERE spotify_uri = '{query.spotifyUri}';"
    user_data = database.execute_query(user_stmt)
    df_user = pd.DataFrame(user_data)

    matches_stmt = f"""
      SELECT *,
      CASE
          WHEN departure_date = '{query.departureDate}' AND return_date = '{query.returnDate}' THEN 'BOTH'
          WHEN departure_date = '{query.departureDate}' THEN 'DEPARTURE'
          WHEN return_date = '{query.returnDate}' THEN 'RETURN'
          ELSE 'NONE'
      END AS match_type
      FROM dataset
      WHERE departure_date = '{query.departureDate}'
      OR return_date = '{query.returnDate}';
    """
    matches_data = database.execute_query(matches_stmt)
    df_potential_matches = pd.DataFrame(matches_data)
    df_potential_matches["compatibility_score"] = (
        (df_potential_matches["danceability"] - df_user["danceability"].values[0]) ** 2
        + (df_potential_matches["energy"] - df_user["energy"].values[0]) ** 2
        + (df_potential_matches["key"] - df_user["key"].values[0]) ** 2
        + (df_potential_matches["loudness"] - df_user["loudness"].values[0]) ** 2
        + (df_potential_matches["instrumentalness"] - df_user["instrumentalness"].values[0]) ** 2
        + (df_potential_matches["liveness"] - df_user["liveness"].values[0]) ** 2
        + (df_potential_matches["valence"] - df_user["valence"].values[0]) ** 2
        + (df_potential_matches["tempo"] - df_user["tempo"].values[0]) ** 2
        + (df_potential_matches["duration_ms"] - df_user["duration_ms"].values[0]) ** 2
        + (df_potential_matches["time_signature"] - df_user["time_signature"].values[0])
        ** 2
    ) ** 0.5

    df_potential_matches = df_potential_matches.sort_values(by='compatibility_score')
    top_matches = df_potential_matches.head(3)
    data_to_insert = top_matches.to_dict(orient='records')

    insert_query = """
        INSERT INTO current_matches (trip_id, traveller_name, departure_city, arrival_city, return_date, departure_date, trip_length, acousticness, danceability, duration_ms, energy, instrumentalness, liveness, loudness, mode, speechiness, tempo, valence, time_signature, key, match_type, compatibility_score)
        VALUES (:trip_id, :traveller_name, :departure_city, :arrival_city, :return_date,:departure_date,:trip_length, :acousticness, :danceability, :duration_ms, :energy, :instrumentalness , :liveness , :loudness, :mode, :speechiness, :tempo, :valence, :time_signature, :key, :match_type, :compatibility_score);
    """

    database.execute_dml_query(insert_query, params=data_to_insert)
