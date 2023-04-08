import requests
from .interface.IApiService import IApiService


class CoinApiService(IApiService):
    @staticmethod
    def get(url: str, params: dict, headers: dict) -> dict:
        return requests.get(url, params=params, headers=headers).json()

    @staticmethod
    def post(url: str, body: dict, headers: dict) -> dict:
        pass
