from flask import Flask
from routes.post_bp import post_bp
from services.post_factory import PostFactory


def create_app(test_config = False):
    app = Flask(__name__)
    app.config.from_object('config')
    with app.app_context():
        if test_config is True:
            PostFactory.create('PostRepo')
        else:
            PostFactory.create('PostDbRepo')
    app.register_blueprint(post_bp, url_prefix='/POST')
    return app