from pydantic import BaseModel
from typing import List


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]


class DataAboutCouriers(BaseModel):
    data: List[Courier]


class CourierId(BaseModel):
    id: int


class ValidationError(BaseModel):
    couriers: List[CourierId]
