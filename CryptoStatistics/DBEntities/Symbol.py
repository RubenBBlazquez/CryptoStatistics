from django.db import models
from ApplicationCore.Services.DB.interface.IDBEntity import IDBEntity


class Symbol(models.Model, IDBEntity):
    symbol = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.symbol

    @staticmethod
    def create_entity(**kwargs):
        if 'symbol' not in kwargs:
            raise Exception('you cannot create a crypto coin entity without the symbol attribute')

        return Symbol(symbol=kwargs['symbol'])

    @staticmethod
    def get_table_name():
        return 'symbol'

    class Meta:
        app_label = 'CryptoStatistics'
