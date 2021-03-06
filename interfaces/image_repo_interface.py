from abc import ABC, abstractmethod


class IImageRepo(ABC):
    @abstractmethod
    def save_image(self, file, filename):
        pass

    @abstractmethod
    def remove_image(self, filename):
        pass
