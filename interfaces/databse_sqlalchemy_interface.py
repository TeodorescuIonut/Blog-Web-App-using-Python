from abc import ABC, abstractmethod


class IDatabaseAlchemy(ABC):
    @abstractmethod
    def generate_engine(self):
        pass

    @abstractmethod
    def generate_session(self):
        pass

    @abstractmethod
    def create_conn(self):
        pass

    @abstractmethod
    def close_and_save(self, conn):
        pass
