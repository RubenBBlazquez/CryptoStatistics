import os
from django.core.management.base import BaseCommand, CommandError
from ApplicationCore.Services.API.ApiService import IApiService, CoinApiService
from ApplicationCore.Services.DB.DBManager import DBManager
from CryptoStatistics.DBEntities.Asks import Asks
from CryptoStatistics.DBEntities.Bids import Bids
from CryptoStatistics.models import Symbol


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.base_api_url = os.getenv('API_URl')
        self.secret_api_key = os.getenv('SECRET_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Token': self.secret_api_key
        }

    def add_arguments(self, parser):
        parser.add_argument('--crypto', type=str)
        parser.add_argument('--real_coin', type=str)

    def handle(self, *args, **options):
        if not options['crypto'] or not options['real_coin']:
            raise CommandError('Parameters [--crypto] and [--real_coin] are obligatory')

        crypto = options['crypto']
        real_coin = options['real_coin']

        crypto_pair = f'{crypto}-{real_coin}'

        crypto_pair_data = CoinApiService.get(f'{self.base_api_url}/{crypto_pair}', {}, self.headers)

        if 'status' in crypto_pair_data and crypto_pair_data['status'] in [500, 404]:
            raise CommandError(f'The pair {crypto_pair} doesnt exists on the API')

        insertion_message = DBManager.insert(crypto_pair_data, Symbol(), [Bids(), Asks()])

        self.stdout.write(insertion_message['message'])
