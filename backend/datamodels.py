from typing import Optional

from pydantic import BaseModel


class Query(BaseModel):
    accessToken: Optional[str] = None
    departureDate: Optional[str] = None
    returnDate: Optional[str] = None
    spotifyUri: Optional[str] = None
