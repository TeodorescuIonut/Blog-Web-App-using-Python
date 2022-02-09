from flask import Flask, render_template
from routes.post_bp import post_bp

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(post_bp, url_prefix='/POST')

@app.route('/')
def main():
    return render_template('blog.html')


if __name__ == "__main__":
    app.run(debug = True)
