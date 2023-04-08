from django.db import models


class IDBEntity:
    @staticmethod
    def create_entity(**kwargs) -> models.Model:
        pass

    @staticmethod
    def get_table_name() -> str:
        pass
