from abc import ABC, abstractmethod


class IPassword(ABC):

    @abstractmethod
    def generate_password(self, password):
        pass

    @abstractmethod
    def check_password(self,hash_password, password):
        pass
