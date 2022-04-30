from abc import ABC, abstractmethod


class IUserStatistics(ABC):

    @abstractmethod
    def get(self):
        pass
