from pydantic import ValidationError
from orders import models
from orders.services import serializer
from couriers.services.serializer import ValidationError
import couriers


def import_orders(json) -> tuple:
    errors = []
    success_ids = []
    success_objects = []
    try:
        orders = serializer.DataAboutOrders.parse_raw(json).data
    except Exception:
        return '{"Error":"Invalid JSON format"}', 400

    for order in orders:
        order_dict = order.dict()
        for field in order_dict.keys():
            if order_dict[field] is None:
                if serializer.OrderId(id=order.order_id) not in errors:
                    errors.append(serializer.OrderId(id=order.order_id))
                break
        else:
            success_objects.append(order)
            success_ids.append(serializer.OrderId(id=order.order_id))
    if len(errors) == 0:
        for dataobject in success_objects:
            if models.Order.create(dataobject=dataobject) == "OK":
                pass
            else:
                return '{"Error":"Invalid JSON format"}', 400
        return serializer.InvalidOrders(orders=success_ids).json(), 201
    else:
        return serializer.ValidationError(ValidationError=serializer.InvalidOrders(orders=errors)).json(), 400


def assign_orders(json) -> tuple:
    try:
        dataobject = serializer.CourierId.parse_raw(json)
        success_orders, assign_time = couriers.models.Delivery.assign_orders(courier_id=dataobject.courier_id)
    except Exception:
        return '{"Error": "invalid json"}', 400

    if assign_time:
        if len(success_orders) == 0 and len(str(assign_time)) == 0:
            return serializer.InvalidOrders(orders=success_orders).json(), 200
        elif len(success_orders) == 0 and len(str(assign_time)) != 0:
            return serializer.AssignOrders(assign_time=str(assign_time), orders=success_orders).json(), 200
        else:
            return serializer.AssignOrders(assign_time=str(assign_time), orders=success_orders).json(), 200
    else:
        return '', 400


def complete_order(json) -> tuple:
    complete_info = serializer.CompleteOrder.parse_raw(json)
    try:
        order = models.Order.objects.get(order_id=complete_info.order_id)
        courier = couriers.models.Courier.objects.get(courier_id=complete_info.courier_id)
    except Exception:
        return '', 400

    if courier.delivery:
        if order not in courier.delivery.orders.all():
            return '', 400

        if courier.delivery.complete_order(order_id=order.order_id, courier_id=courier.courier_id,
                                           date_of_complete=complete_info.complete_time) == 'OK':
            return complete_info.json(include={'order_id'}), 200

        else:
            return '', 400

    return '', 400

