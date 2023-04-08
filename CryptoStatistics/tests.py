import os
from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase
from ApplicationCore.Services.API.ApiService import CoinApiService
from ApplicationCore.Services.DB.DBManager import DBManager
from ApplicationCore.Utils import Utils
from CryptoStatistics.DBEntities.Asks import Asks
from CryptoStatistics.DBEntities.Bids import Bids
from CryptoStatistics.DBEntities.Symbol import Symbol
from CryptoStatistics.models import CryptoStatistics
from CryptoStatistics.Enums.OrderTypesEnum import OrderTypes
from django.core.exceptions import ObjectDoesNotExist


class DatabaseInsertionsTestCase(TestCase):
    def test_insert_good_raw_data_on_insert_method_from_db_manager(self):
        raw_default_data = {
            'symbol': 'BTC-USD',
            'bids': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
            'asks': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
        }
        good_insert_message = {'message': 'all data was inserted successfully'}

        insert_message = DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])

        self.assertDictEqual(good_insert_message, insert_message)

    def test_insert_bad_raw_data_on_insert_method_from_db_manager(self):
        raw_default_data = {
            'symbol2': 'BTC-USD',
            'bids98': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
            'asks12': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
        }

        insert_message = DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])

        self.assertIn('message', insert_message.keys())
        self.assertIn('Error', insert_message['message'])


class GetDataFromDatabaseTestCase(TestCase):
    def setUp(self) -> None:
        raw_default_data = {
            'symbol': 'BTC-USD',
            'bids': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
            'asks': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
        }

        DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])
        DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])

    def test_is_get_method_from_db_ok(self):
        symbol_filter = 'BTC-USD'
        symbol_entity = DBManager.get(Symbol, ('symbol', symbol_filter))

        self.assertIsInstance(symbol_entity, Symbol)
        self.assertEqual(symbol_entity.symbol, symbol_filter)

    def test_get_method_with_no_data_found(self):
        symbol_filter = 'ETH-USD'

        self.assertRaises(ObjectDoesNotExist, DBManager.get, Bids, ('symbol', symbol_filter))

    def test_is_get_all_method_from_db_ok(self):
        symbol_filter = 'BTC-USD'
        bids = DBManager.get_all(Bids, ('symbol', symbol_filter))

        self.assertGreater(len(bids), 0)

    def test_get_all_method_with_no_data_found(self):
        symbol_filter = 'ETH-USD'

        self.assertRaises(ObjectDoesNotExist, DBManager.get_all, Bids, ('symbol', symbol_filter))


class CryptoStatisticsTestCase(TestCase):
    def setUp(self) -> None:
        raw_default_data = {
            'symbol': 'BTC-USD',
            'bids': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
            'asks': {
                'qty': '1',
                'num': '10000',
                'px': '30000'
            },
        }

        DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])

        raw_default_data['symbol'] = 'ETH-USD'

        DBManager.insert(raw_default_data, Symbol(), [Bids(), Asks()])

    def test_get_bids_statistics_with_existing_symbol_in_db(self):
        symbol_that_exists = 'BTC-USD'
        bids_default_structure = {
            'bids': {
                'average_value': float,
                'greater_value': {'px': float, 'qty': float, 'num': float, 'value': float},
                'lesser_value': {'px': float, 'qty': float, 'num': float, 'value': float},
                'total_qty': float,
                'total_px': float
            }
        }

        crypto_information = CryptoStatistics.get_statistics_by_order_type_and_symbol(
            str(OrderTypes.BIDS.value),
            symbol_that_exists
        )

        information_formatted = Utils.replace_dict_values_to_type(crypto_information)

        self.assertDictEqual(information_formatted, bids_default_structure)

    def test_get_asks_statistics_with_existing_symbol_in_db(self):
        symbol_that_exists = 'BTC-USD'
        asks_default_structure = {
            'asks': {
                'average_value': float,
                'greater_value': {'px': float, 'qty': float, 'num': float, 'value': float},
                'lesser_value': {'px': float, 'qty': float, 'num': float, 'value': float},
                'total_qty': float,
                'total_px': float
            }
        }

        crypto_information = CryptoStatistics.get_statistics_by_order_type_and_symbol(
            str(OrderTypes.ASKS.value),
            symbol_that_exists
        )

        information_formatted = Utils.replace_dict_values_to_type(crypto_information)

        self.assertDictEqual(information_formatted, asks_default_structure)

    def test_get_statistics_from_bids_with_non_existing_symbol_in_db(self):
        symbol_that_not_exists = 'BTCCC-USD'

        self.assertRaises(
            ObjectDoesNotExist,
            CryptoStatistics.get_statistics_by_order_type_and_symbol,
            str(OrderTypes.BIDS.value),
            symbol_that_not_exists
        )

    def test_get_general_statistics(self):
        internal_default_structure = {
            'bids': {
                'count': float,
                'qty': float,
                'value': float
            },
            'asks': {
                'count': float,
                'qty': float,
                'value': float
            }
        }
        general_default_structure = {
            'BTC-USD': internal_default_structure,
            'ETH-USD': internal_default_structure
        }

        crypto_information = CryptoStatistics.get_general_statistics()

        information_formatted = Utils.replace_dict_values_to_type(crypto_information)

        self.assertDictEqual(information_formatted, general_default_structure)


class SaveCoinCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.valid_api_url = os.getenv('API_URL')
        self.default_headers = {
            'Content-Type': 'application/json',
            'X-API-Token': os.getenv('SECRET_API_KEY')
        }

    def test_valid_api_key_and_url(self):
        api_information = CoinApiService.get(f'{self.valid_api_url}/BTC-USD', {}, self.default_headers)

        self.assertNotIn('status', api_information)

    def test_valid_parameters(self):
        out = StringIO()
        call_command('save_coin', symbol='BTC', real_coin='USD', stdout=out)

        self.assertIn('success', out.getvalue())

    def test_not_valid_parameters(self):
        self.assertRaises(
            TypeError,
            call_command,
            'save_coin',
            symbol23='BTC',
            real_coin='USD'
        )

        self.assertRaises(
            CommandError,
            call_command,
            'save_coin',
        )

    def test_symbol_and_real_coin_dont_exists_on_API(self):
        self.assertRaises(
            CommandError,
            call_command,
            'save_coin',
            symbol='BTCCC',
            real_coin='USD'
        )
