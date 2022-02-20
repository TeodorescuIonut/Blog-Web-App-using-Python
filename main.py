from flask import Flask
from routes.post_bp import ConstructBP
from services.post_factory import PostFactory


def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config')
    repo = PostFactory.create(test_config)
    post_bp = ConstructBP(repo).post_bp
    app.register_blueprint(post_bp, url_prefix='/POST')
    return app