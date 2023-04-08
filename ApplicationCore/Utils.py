import json

from django.core import serializers
from django.db.models import QuerySet


class Utils:
    @staticmethod
    def deserialize_orm_object(objects: QuerySet) -> dict:
        try:
            return json.loads(serializers.serialize('json', objects))
        except Exception:
            raise Exception('You are trying to deserialize a non orm object')

    @staticmethod
    def replace_dict_values_to_type(information: dict) -> dict:
        for key in information.keys():
            if type(information[key]) == dict:
                Utils.replace_dict_values_to_type(information[key])

                continue

            information[key] = type(information[key])

        return information
