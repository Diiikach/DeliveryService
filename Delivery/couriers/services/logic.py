import json
from couriers.services import serializer
from pydantic import ValidationError
from couriers import models


def import_couriers(content) -> tuple:
    """
    This function parses the entry
    point for creating
    entities in the database
    and catching errors.
    :param content:
    :return tuple:
    """
    return get_couriers_or_errors(content)


def get_full_courier_info(courier_id) -> tuple:
    try:
        courier = models.Courier.get_py_dantic_from_django_model(courier_id=courier_id, advanced=True)
    except Exception:
        return '', 404
    if courier.rating == 0.0:
        return courier.json(exclude={'rating'}), 200
    else:
        return courier.json(), 200


def get_couriers_or_errors(content) -> tuple:
    errors = []
    try:
        couriers = serializer.DataAboutCouriers.parse_raw(content)
    except Exception as E:
        return '{"Error":"Invalid JSON format"}', 400

    dict_couriers = couriers.dict()['data']
    for courier in dict_couriers:
        for key in courier.keys():
            if courier[key] is None:
                if serializer.CourierId(id=courier['courier_id']) not in errors:
                    errors.append(serializer.CourierId(id=courier['courier_id']))

    if len(errors) == 0:
        create_courier_object_from_collection(couriers)
        return serializer.ResponseCouriers(couriers=[serializer.CourierId(id=courier.courier_id) for courier in couriers.data]).json(), 201
    else:
        return serializer.ValidationError(ValidationError=serializer.Error(couriers=errors)).json(), 400


def create_courier_object_from_collection(collection) -> str:
    for courier in collection.data:
        models.Courier.create(dantic_object=courier)
    return "OK"


def change_courier_info(courier_id, content):
    dantic_model: dict = models.Courier.get_py_dantic_from_django_model(courier_id=courier_id).dict()
    try:
        changing_fields: dict = json.loads(content)
    except json.decoder.JSONDecodeError as E:
        return "{'Error': 'Invalid json format'}", 400

    for key in changing_fields:
        dantic_model[key] = changing_fields[key]

    try:
        dantic_model = serializer.Courier.parse_obj(dantic_model)
    except ValidationError:
        return "{'Error': 'Invalid json format'}", 400

    changed = models.Courier.change_courier(dantic_object=dantic_model, courier_id=courier_id)
    if changed == 'OK':
        return dantic_model.json(), 200
    else:
        return changed, 400
