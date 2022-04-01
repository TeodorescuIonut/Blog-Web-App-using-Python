from abc import ABC, abstractmethod


class IFiltering(ABC):
   
    @abstractmethod
    def return_filter(self):
        pass

    @abstractmethod
    def get_owner_id(self):
        pass