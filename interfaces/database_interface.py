import abc


class IDatabase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_conn(self):
           pass
    @abc.abstractmethod   
    def create_cursor(self):
        pass
    @abc.abstractmethod
    def close_and_save(self, conn,cur):
        pass
