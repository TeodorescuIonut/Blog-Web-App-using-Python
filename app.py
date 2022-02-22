from databases.database_manager import Database
from databases.database_bp import database_bp, db_setup
from main import create_app
from flask import redirect, render_template, url_for



app = create_app()

@app.before_request
def before_request_func():    
    if Database.configured is False:   
        return redirect(url_for('database_bp.db_setup'))

    return render_template('blog.html')
    
@app.route('/')
def main():
    
    return render_template('blog.html')
    

if __name__ == "__main__":
    app.run(debug = False)





