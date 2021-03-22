from pydantic import BaseModel
from types import list


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: list[int]
    working_hours: list[str]


class DataAboutCouriers(BaseModel):
    data: list
