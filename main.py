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

from databases.database_manager import Database
from databases.database_bp import database_bp



def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(database_bp)
    # @app.before_first_request
    # def before_first_request():      
    #    if DatabaseConfig().is_configured is False:
    #         return redirect(url_for('database_bp.setup'))
    from services.post_factory import PostFactory
    repo = PostFactory.create(test_config)
    post_bp = PostBlueprint(repo).create()
    app.register_blueprint(post_bp, url_prefix='/POST')
    
    return app