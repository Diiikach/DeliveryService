from pydantic import BaseModel, validator
from pydantic import BaseModel, validator
from typing import List


class Courier(BaseModel):
    """
    'Courier' is Pydantic object, which serialize json structuru
    to python dataclass.
    """
    courier_id: int
    courier_type: str
    regions: List[int]
    working_hours: List[str]

    @validator('working_hours')
    def must_be_more_than_one_in_wh(cls, wh):
        if len(wh) == 0:
            raise ValidationError
        else:
            return wh

    @validator('regions')
    def must_be_more_than_one_in_regions(cls, r):
        if len(r) == 0:
            raise ValidationError
        else:
            return r


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
