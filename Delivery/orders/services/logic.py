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
        if len(success_orders) == 0:
            return serializer.InvalidOrders(orders=success_orders).json(), 200
        else:
            return serializer.AssignOrders(assign_time=assign_time, orders=success_orders).json(), 200
    else:
        return '', 400


def complete_order(json) -> tuple:
    complete_info = serializer.CompleteOrder.parse_raw(json)
    try:
        order = models.Order.objects.get(order_id=complete_info.order_id)
        courier = couriers.models.Courier.objects.get(courier_id=complete_info.courier_id)
    except Exception:
        return '', 400

    if order not in courier.delivery.orders.all():
        return '', 400

    if couriers.models.Delivery.complete_order(order_id=order.order_id, courier_id=courier.courier_id,
                                               assign_time=complete_info) == 'OK':
        return complete_info.json(include={'order_id'}), 200
