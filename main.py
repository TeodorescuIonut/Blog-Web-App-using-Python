from flask import Flask
import sys
import os
from pathlib import Path



myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from services.service import ContainerService
from routes.post_bp import PostBlueprint
from databases.database_bp import database_bp



def create_app(test_config = False):

    app = Flask(__name__)
    app.config.from_object('config') 
    ContainerService.testing_config = test_config
    post_bp = PostBlueprint().create()
    app.register_blueprint(database_bp)
    app.register_blueprint(post_bp, url_prefix='/POST')

    return app