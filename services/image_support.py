import os

from interfaces.image_support_interface import IImageSupport


class ImageSupport(IImageSupport):
    def save_image(self, file, filename):
        if file:
            path = os.path.join(os.path.abspath('./static/images'), filename)
            file.save(path)
