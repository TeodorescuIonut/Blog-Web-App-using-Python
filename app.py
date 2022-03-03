import sys
import os
from pathlib import Path

from decorators.decorators import check_setup
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from main import create_app
from flask import redirect, render_template, request, url_for
from databases.database_config import DatabaseConfig
from databases.database_bp import database_bp, setup


app = create_app() 

@app.route('/')
@check_setup
def main():
    return render_template('blog.html')


if __name__ == "__main__":
    app.run(port = 5000, debug = False)
