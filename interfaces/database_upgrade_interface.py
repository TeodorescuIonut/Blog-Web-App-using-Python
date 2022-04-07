from abc import ABC, abstractmethod


class IDatabaseUpgrade(ABC):

    @abstractmethod
    def upgrade_db(self):
        pass

    @abstractmethod
    def is_latest_db_version(self):
        pass
