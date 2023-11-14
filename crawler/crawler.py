import abc

class Crawler(metaclass=abc.ABCMeta):
    def __init__(self, db_params) -> None:
        self._db_params = db_params
        self._metadata_str = ''
        self._db_dict = {}

    @abc.abstractmethod
    def explore_db(self):
        pass
    
    @abc.abstractmethod
    def export_metadata_to_file(self):
        pass

    @abc.abstractmethod
    def get_db_dict(self):
        pass