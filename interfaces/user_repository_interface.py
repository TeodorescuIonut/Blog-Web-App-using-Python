import abc

class IUserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, user_id):
        raise NotImplementedError
    @abc.abstractmethod
    def create(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user):
        raise NotImplementedError
    @abc.abstractmethod
    def get_user_by_email(self, user_email):
        raise NotImplementedError

    @abc.abstractmethod
    def check_user_email(self,user_to_check)-> bool:
        raise NotImplementedError
