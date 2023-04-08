from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import QuerySet
from ApplicationCore.Services.DB.interface.IDBManager import IDBManager
from django.db.models import Q
from ApplicationCore.Services.DB.interface.IDBEntity import IDBEntity


class DBManager(IDBManager):
    @staticmethod
    def get(entity: Type[models.Model], filter_param: tuple) -> QuerySet:
        try:
            return entity.objects.get(Q(filter_param))
        except Exception:
            raise ObjectDoesNotExist(f'There is no data with the {filter_param[0]} {filter_param[1]} you just used')

    @staticmethod
    def get_all(entity: Type[models.Model], filter_param: tuple) -> QuerySet:
        if not filter_param:
            return entity.objects.all()

        entity_data = entity.objects.all().filter(Q(filter_param))

        if len(entity_data) == 0:
            raise ObjectDoesNotExist(f'There is no data with the {filter_param[0]} {filter_param[1]} you just used')

        return entity_data

    @staticmethod
    def insert(raw_data: dict, entity: IDBEntity, foreign_entities: list[IDBEntity]) -> dict:
        try:
            if entity.get_table_name() not in raw_data.keys():
                raise Exception(f'{entity.get_table_name()} is obligatory to create {entity.get_table_name()} Objects')

            main_entity = entity.create_entity(**raw_data)
            main_entity.save()

            for foreign_entity in foreign_entities:
                if foreign_entity.get_table_name() not in raw_data.keys():
                    raise Exception(
                        f'{foreign_entity.get_table_name()} is obligatory to create {foreign_entity.get_table_name()} Objects')

                foreign_entity_data = raw_data[foreign_entity.get_table_name()]

                if type(foreign_entity_data) == dict:
                    foreign_data = {**foreign_entity_data, entity.get_table_name(): main_entity}
                    foreign_entity.create_entity(**foreign_data).save()

                    continue

                for entity_data in raw_data[foreign_entity.get_table_name()]:
                    foreign_data = {**entity_data, entity.get_table_name(): main_entity}
                    foreign_entity.create_entity(**foreign_data).save()

            return {'message': 'all data was inserted successfully'}

        except Exception as err:
            return {'message': f'Error: {str(err)}'}
