import base64

from interfaces.image_memory_repo_interface import IImageMemoryRepo


class ImageMemoryRepo(IImageMemoryRepo):
    def save_image(self, image):
        if image:
            image_64_encode = base64.b64encode(image.read()).decode('utf-8')
            return image_64_encode
