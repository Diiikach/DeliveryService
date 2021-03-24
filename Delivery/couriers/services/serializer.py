from typing import List
from pydantic import BaseModel, validator
from couriers import models


class Courier(BaseModel):
    """
    'Courier' is Pydantic object, which serialize json structuru
    to python dataclass.
    """
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]

    @validator('working_hours', allow_reuse=True)
    def must_be_more_than_one_in_wh(cls, wh):
        if len(wh) == 0:
            raise ValidationError
        else:
            return wh

    @validator('regions', allow_reuse=True)
    def little_length(cls, r):
        if len(r) == 0:
            raise ValidationError
        else:
            return r


class DataAboutCouriers(BaseModel):
    data: List[Courier]


class CourierId(BaseModel):
    id: int


class AdvancedCourier(Courier):
    rating: float
    earning: int

class ResponseCouriers(BaseModel):
    couriers: List[CourierId]


class Error(BaseModel):
    couriers: List[CourierId]


class ValidationError(BaseModel):
    ValidationError: Error
