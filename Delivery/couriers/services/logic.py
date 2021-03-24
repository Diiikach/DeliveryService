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
    :param json:
    :return tuple:
    """
    return get_couriers_or_errors(content)


def get_full_courier_info(courier_id) -> tuple:
    courier = models.Courier.get_py_dantic_from_django_model(courier_id=courier_id, advanced=True)
    if courier.rating == 0.0:
        return courier.json(exclude={'earning'}), 201
    else:
        return courier.json()


def get_couriers_or_errors(content) -> tuple:
    _errors = []
    sucess = []
    python_dict = json.loads(content)
    try:
        couriers = serializer.DataAboutCouriers.parse_raw(content)
    except ValidationError as error:
        for e in error.errors():
            _errors.append(serializer.CourierId(id=python_dict['data'][e['loc'][1]]['courier_id']))

    else:
        if create_courier_object_from_collection(couriers) == "OK":

            for courier in couriers.data:
                sucess.append(serializer.CourierId(id=courier.courier_id))
            return serializer.ResponseCouriers(couriers=sucess).json(), 201

    if len(_errors) > 0:
        errors = serializer.ValidationError(ValidationError=serializer.Error(couriers=_errors))
        return errors.json(), 400


def create_courier_object_from_collection(collection) -> str:
    for courier in collection.data:
        models.Courier.create(courier)

    return "OK"


