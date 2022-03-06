from pydantic import BaseModel


class Link(BaseModel):
    id: int
    name: str
