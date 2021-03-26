from pydantic import ValidationError
from orders import models
from orders.services import serializer
from couriers.services.serializer import ValidationError
import couriers


def import_orders(json) -> tuple:
    errors = []
    success_ids = []
    success_objects = []
    orders = serializer.DataAboutOrders.parse_raw(json).data
    for order in orders:
        order_dict = order.dict()
        for field in order_dict.keys():
            if order_dict[field] is None:
                errors.append(serializer.OrderId(id=order.order_id))
                break
        else:
            success_objects.append(order)
            success_ids.append(serializer.OrderId(id=order.order_id))
    if len(errors) == 0:
        for dataobject in success_objects:
            models.Order.create(dataobject=dataobject)
        return serializer.InvalidOrders(orders=success_ids).json(), 201
    else:
        return serializer.ValidationError(ValidationError=serializer.InvalidOrders(orders=errors)).json(), 400


def assign_orders(json) -> tuple:
    dataobject = serializer.CourierId.parse_raw(json)
    success_orders, assign_time = couriers.models.Delivery.assign_orders(courier_id=dataobject.courier_id)
    if assign_time:
        print(success_orders)
        return serializer.AssignOrders(assign_time=assign_time, orders=success_orders).json(), 200
    else:
        return '', 400

