from abc import abstractmethod
from abc import ABCMeta
from django.db import models
from django.db.models import QuerySet


class IDBManager(ABCMeta):
    @staticmethod
    @abstractmethod
    def get_all(entity: models.Model, filter_param: tuple) -> QuerySet:
        pass

    @staticmethod
    @abstractmethod
    def get(entity: models.Model, filter_param: tuple) -> QuerySet:
        pass

    @staticmethod
    @abstractmethod
    def insert(raw_data: dict, entity: models.Model, foreign_entities: list[models.Model]) -> bool:
        pass
