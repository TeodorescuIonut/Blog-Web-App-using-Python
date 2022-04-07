from abc import ABC, abstractmethod


class IAuthentication(ABC):

    @abstractmethod
    def sign_in(self, user_email, password):
        pass

    @abstractmethod
    def get_user_details(self):
        pass

    @abstractmethod
    def sign_out(self):
        pass

    @abstractmethod
    def is_logged_in(self):
        pass
