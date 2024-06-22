from typing import Optional

from pydantic import BaseModel


class BaseClientData(BaseModel):
    pass


class ClientData(BaseClientData):
    accessToken: Optional[str] = None
    checked: list[str]
    stopPlayback: Optional[bool] = False
    tempo: Optional[int] = None
