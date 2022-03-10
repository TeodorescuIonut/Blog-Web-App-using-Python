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