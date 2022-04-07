
from flask import Flask
from services.service import ContainerService
from routes.post_bp import PostBlueprint
from routes.user_bp import UserBlueprint
from routes.authentication_bp import authenticate
from databases.database_bp import database_bp


def create_app(test_config=False):
    app = Flask(__name__)
    app.config.from_object('config')
    ContainerService.testing_config = test_config
    post_bp = PostBlueprint().create()
    user_bp = UserBlueprint().create()
    app.register_blueprint(database_bp)
    app.register_blueprint(authenticate)
    app.register_blueprint(post_bp, url_prefix='/POST')
    app.register_blueprint(user_bp, url_prefix='/USER')
    return app
