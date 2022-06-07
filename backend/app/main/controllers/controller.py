from flask_restplus import reqparse
from app.main.services.cache_manager import CacheManager
from app.main.utils.es_connection import ESConnection
from abc import ABC, abstractmethod

cache_manager = CacheManager()
es = ESConnection()


class Controller(ABC):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.cache_manager = cache_manager
        self.es = es
        super().__init__()

    @abstractmethod
    def _add_args(self):
        pass

    def _parse_args(self):
        self.args = self.parser.parse_args()

    @abstractmethod
    def process_args(self):
        pass
