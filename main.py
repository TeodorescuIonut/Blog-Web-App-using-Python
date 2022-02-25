import sys
import os
from pathlib import Path
from databases.database_config import DatabaseConfig
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from flask import Flask, redirect, url_for
from routes.post_bp import PostBlueprint
from services.post_factory import PostFactory
from databases.database_manager import Database
from databases.database_bp import database_bp




def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config') 
    repo = PostFactory.create(test_config)
    post_bp = PostBlueprint(repo).create()
    app.register_blueprint(post_bp, url_prefix='/POST')
    app.register_blueprint(database_bp)

    return app