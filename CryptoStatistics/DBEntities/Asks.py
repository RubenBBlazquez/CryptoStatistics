from typing import Type

from django.db import models
from CryptoStatistics.DBEntities.Symbol import Symbol
from ApplicationCore.Services.DB.interface.IDBEntity import IDBEntity


class Asks(models.Model, IDBEntity):
    px = models.FloatField()
    qty = models.FloatField()
    num = models.IntegerField()
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ask from COIN {self.symbol} with px:{self.px}, qty:{self.qty}, num: {self.num}'

    @staticmethod
    def create_entity(**kwargs):
        not_valid_kwards = 'symbol' not in kwargs or 'px' not in kwargs or 'qty' not in kwargs or 'num' not in kwargs

        if not_valid_kwards:
            raise Exception('you cannot create an asks entity without any of the px, qty, num, symbol attributes')

        return Asks(px=kwargs['px'], qty=kwargs['qty'], num=kwargs['num'], symbol=kwargs['symbol'])

    @staticmethod
    def get_table_name():
        return 'asks'

    class Meta:
        app_label = 'CryptoStatistics'
