import sys
import os
from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from databases.database_bp import database_bp, setup
from main import create_app
from flask import redirect, render_template, url_for
from databases.database_config import DatabaseConfig


app = create_app() 

@app.before_first_request
def before_func():
    if DatabaseConfig().is_configured() is False:
        return redirect(url_for('database_bp.setup'))
  
@app.route('/')
def main():
    return render_template('blog.html')
    
if __name__ == "__main__":
    app.run(debug = False)