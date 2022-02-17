from flask import Flask
from routes.post_bp import construct_bp
from services.post_factory import PostFactory


def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config')
    if test_config is True:
        repo = PostFactory.create('PostRepo')
    else:
        repo =  PostFactory.create('PostDbRepo')
    post_bp = construct_bp(repo)
    app.register_blueprint(post_bp, url_prefix='/POST')
    return app