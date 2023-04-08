from abc import abstractmethod
from abc import ABCMeta


class IApiService(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get(url: str, params: dict, headers: dict) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def post(url: str, body: dict, headers: dict) -> dict:
        pass
