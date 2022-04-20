import base64
from static.default_post_image.image_seed import IMAGE_DATA

from interfaces.image_repo_interface import IImageRepo


class ImageMemoryRepo(IImageRepo):
    def save_image(self, image):
        if image:
            image_64_encode = base64.b64encode(image.read()).decode('utf-8')
            return image_64_encode
        else:
            return IMAGE_DATA

    def remove_image(self, filename):
        pass
