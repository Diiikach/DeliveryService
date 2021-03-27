from typing import List
from pydantic import BaseModel, validator, Field
from couriers import models


class Courier(BaseModel):
    """
    'Courier' is Pydantic object, which serialize json structuru
    to python dataclass.
    """
    courier_id: int = Field(default=None)
    courier_type: str = Field(default=None)
    regions: List[int] = Field(default=None)
    working_hours: List[str] = Field(default=None)

    @validator('working_hours', allow_reuse=True)
    def must_be_more_than_one_in_wh(cls, wh):
        if wh:
            if len(wh) == 0:
                raise ValidationError
            else:
                return wh
        return None

    @validator('regions', allow_reuse=True)
    def little_length(cls, r):
        if r:
            if len(r) == 0:
                raise ValidationError
            else:
                return r
        return r


class AdvancedCourier(Courier):
    rating: float
    earning: int


class DataAboutCouriers(BaseModel):
    data: List[Courier]


class CourierId(BaseModel):
    id: int


class ResponseCouriers(BaseModel):
    couriers: List[CourierId]


class Error(BaseModel):
    couriers: List[CourierId]


class ValidationError(BaseModel):
    ValidationError: Error
