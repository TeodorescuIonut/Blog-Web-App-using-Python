from threading import Thread
from main import create_app
from flask import render_template, request

app = create_app()

@app.route('/')
def main():
    return render_template('blog.html')

if __name__ == "__main__":
    app.run(debug = False)





