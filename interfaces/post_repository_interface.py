import abc


class IPostRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_all(self, per_page, offset, selected_owner_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, post_id):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, post):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, post):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, post):
        raise NotImplementedError
