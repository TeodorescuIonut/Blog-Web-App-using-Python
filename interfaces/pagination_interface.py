from abc import ABC, abstractmethod


class IPagination(ABC):
    @abstractmethod
    def current_page(self):
        pass

    @abstractmethod
    def offset(self):
        pass

    @abstractmethod
    def set_pagination(self, count):
        pass

    @abstractmethod
    def set_no_per_page(self, no_per_page):
        pass
