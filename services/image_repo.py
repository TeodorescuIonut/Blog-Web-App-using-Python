import os

from interfaces.image_repo_interface import IImageRepo


class ImageRepo(IImageRepo):
    upload_path = '/static/images/'
    default_image_path = '/static/default_post_image/default.jpg'

    def remove_image(self, filename):
        if filename != '' and filename is not None:
            path = f".{self.upload_path}" + filename
            if os.path.exists(path):
                os.remove(path)
            else:
                print('The file doesnt exists')

    def save_image(self, file, filename):
        if file:
            path = os.path.join(os.path.abspath(f".{self.upload_path}"), filename)
            file.save(path)
            file.filename = self.upload_path + filename
        if filename == '':
            file.filename = self.default_image_path
