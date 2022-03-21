from abc import ABC, abstractmethod



class IDatabaseUpgrade(ABC):

    @abstractmethod
    def upgrade_db(self):
        pass