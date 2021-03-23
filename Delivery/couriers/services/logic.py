from couriers.services import serializer
from pydantic import ValidationError
from couriers import models


def import_couriers(json) -> tuple:
    """
    This function parses the entry
    point for creating
    entities in the database
    and catching errors.
    :param json:
    :return tuple:
    """
    return get_couriers_or_errors(json)


def get_couriers_or_errors(json) -> tuple:
    _errors = []
    sucess = []
    try:
        couriers = serializer.DataAboutCouriers.parse_raw(json)
    except ValidationError as error:
        print(error.errors()[0])
        _errors.append(serializer.CourierId(id=error.errors()[0]['loc'][1]))
    else:
        if create_courier_object_from_collection(couriers) == "OK":
            return couriers.json(), 201

    if len(_errors) > 0:
        errors = serializer.ValidationError(couriers=_errors)
        return errors.json(), 400


def create_courier_object_from_collection(collection) -> str:
    for object in collection.data:
        models.Courier.create(object)

    return "OK"


