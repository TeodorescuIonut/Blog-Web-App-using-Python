import sys
import os
from pathlib import Path
from decorators.injector_di import injector

from decorators.setup import check_setup
from interfaces.authentication_interface import IAuthentication
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from main import create_app
from flask import g, redirect, render_template, url_for



app = create_app() 
    
@app.route('/')
@check_setup
def main():
    return redirect(url_for('post_bp.blog'))


if __name__ == "__main__":
    app.run(port = 5000, debug = False)
