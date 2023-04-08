from typing import Type

import numpy as np
import pandas as pd
from django.db import models
from ApplicationCore.Services.DB.DBManager import DBManager
from ApplicationCore.Utils import Utils
from CryptoStatistics.DBEntities.Asks import Asks
from CryptoStatistics.DBEntities.Bids import Bids
from CryptoStatistics.DBEntities.Symbol import Symbol
from CryptoStatistics.Enums.OrderTypesEnum import OrderTypes


class CryptoStatistics:
    @staticmethod
    def clean_dataset(json_object: dict) -> pd.DataFrame:
        dataframe = pd.DataFrame(json_object)

        dataframe.drop(['model', 'pk'], inplace=True, axis=1)

        dataframe = dataframe.apply(
            lambda json_row: pd.Series(json_row[0]),
            axis=1,
        )

        dataframe.drop(['symbol'], inplace=True, axis=1)

        return dataframe

    @staticmethod
    def get_statistics_by_order_type_and_symbol(order_type: str, crypto_symbol: str) -> dict:
        if order_type == OrderTypes.BIDS.value:
            return {order_type: CryptoStatistics.get_basic_statistics(Bids, crypto_symbol)}

        return {order_type: CryptoStatistics.get_basic_statistics(Asks, crypto_symbol)}

    @staticmethod
    def get_basic_statistics(entity: Type[models.Model], crypto_symbol: str) -> dict:
        entity_json = Utils.deserialize_orm_object(
            DBManager.get_all(entity, ('symbol', crypto_symbol))
        )
        dataframe = CryptoStatistics.clean_dataset(entity_json).astype(float)

        dataframe['value'] = dataframe['qty'] * dataframe['px']

        average_value = dataframe['value'].mean()

        greater_value_index = np.argmax(dataframe['value'])
        greater_value = dataframe.iloc[greater_value_index]

        lesser_value_index = np.argmin(dataframe['value'])
        lesser_value = dataframe.iloc[lesser_value_index]

        total_qty = dataframe['qty'].sum()
        total_px = dataframe['px'].sum()

        return {
            'average_value': float(average_value),
            'greater_value': greater_value.to_dict(),
            'lesser_value': lesser_value.to_dict(),
            'total_qty': float(total_qty),
            'total_px': float(total_px)
        }

    @staticmethod
    def get_general_statistics():
        all_coins = DBManager.get_all(Symbol, ())
        all_coins_json = Utils.deserialize_orm_object(all_coins)

        general_statistics = {}

        for coin in all_coins_json:
            coin_symbol = coin['pk']

            general_statistics[coin_symbol] = CryptoStatistics.get_general_statistics_from_one_symbol(coin_symbol)

        return general_statistics

    @staticmethod
    def get_general_statistics_from_one_symbol(crypto_coin_id: int) -> dict:
        bids = DBManager.get_all(Bids, ('symbol', crypto_coin_id))
        asks = DBManager.get_all(Asks, ('symbol', crypto_coin_id))

        bids_json = Utils.deserialize_orm_object(bids)
        asks_json = Utils.deserialize_orm_object(asks)

        bids_dataframe = CryptoStatistics.clean_dataset(bids_json).astype(np.float32)
        asks_dataframe = CryptoStatistics.clean_dataset(asks_json).astype(np.float32)

        total_bids = bids_dataframe.shape[0]
        total_asks = asks_dataframe.shape[0]

        total_value_bids = (bids_dataframe['qty'] * bids_dataframe['px']).sum()
        total_value_asks = (asks_dataframe['qty'] * asks_dataframe['px']).sum()

        coin_qty_bids = bids_dataframe['qty'].sum()
        coin_qty_asks = asks_dataframe['qty'].sum()

        return {
            'bids': {
                'count': float(total_bids),
                'value': float(total_value_bids),
                'qty': float(coin_qty_bids),
            },
            'asks': {
                'count': float(total_asks),
                'value': float(total_value_asks),
                'qty': float(coin_qty_asks),
            }
        }
