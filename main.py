from flask import Flask, redirect, url_for
from routes.post_bp import ConstructBP
from services.post_factory import PostFactory
from databases.database_manager import Database
from databases.database_bp import database_bp,db_setup


def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config')
    repo = PostFactory.create(test_config)  
    post_bp = ConstructBP(repo).post_bp
    app.register_blueprint(database_bp) 
    app.register_blueprint(post_bp, url_prefix='/POST')
    return app