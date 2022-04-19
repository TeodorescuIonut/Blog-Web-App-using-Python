from abc import ABC, abstractmethod


class IImageMemoryRepo(ABC):
    @abstractmethod
    def save_image(self, image):
        pass
