from abc import ABC, abstractmethod


class IImageSupport(ABC):
    @abstractmethod
    def save_image(self, file, filename):
        pass
