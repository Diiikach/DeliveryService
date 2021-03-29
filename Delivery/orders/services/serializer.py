from typing import List
from pydantic import BaseModel, Field, validator


class Order(BaseModel):
    order_id: int = Field(default=None)
    weight: float = Field(default=None)
    region: int = Field(default=None)
    delivery_hours: List[str] = Field(default=None)

    @validator('delivery_hours')
    def must_be_more_than_one_in_wh(cls, dh):
        if not dh:
            return dh
        if len(dh) == 0:
            dh = None
        return dh


class OrderId(BaseModel):
    id: int


class InvalidOrders(BaseModel):
    orders: List[OrderId]


class DataAboutOrders(BaseModel):
    data: List[Order]


class ValidationError(BaseModel):
    ValidationError: InvalidOrders


class AssignOrders(BaseModel):
    orders: List[OrderId] = Field(default=None)
    assign_time: str = Field(default=None)


class CourierId(BaseModel):
    courier_id: int


class CompleteOrder(BaseModel):
    courier_id: int
    order_id: int
    complete_time: str
