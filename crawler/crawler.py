import abc

class Crawler(metaclass=abc.ABCMeta):
    def __init__(self, dbname, user, password, host, port) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self._db_params = {'dbname': dbname, 'user': user, 'password': password, 'host': host, 'port': port}
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