from pydantic import BaseModel
from types import list


class Order(BaseModel):
    order_id: int
    weight: float
    regions: int
    working_hours: list[str]


class DataAboutOrders(BaseModel):
    data: list
