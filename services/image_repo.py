import os

from interfaces.image_repo_interface import IImageRepo


class ImageRepo(IImageRepo):
    def remove_image(self, filename):
        if filename != '' and filename is not None:
            path = './static/images/' + filename
            if os.path.exists(path):
                os.remove(path)
            else:
                print('The file doesnt exists')

    def save_image(self, file, filename):
        if file:
            path = os.path.join(os.path.abspath('./static/images'), filename)
            file.save(path)
