from pydantic import BaseModel


class Query(BaseModel):
    accessToken: str