from distutils.log import debug
from flask import Flask, render_template, request
from datetime import datetime
import re

app = Flask(__name__)

myList = []
class post: 
    def __init__(self, id, title, contents, ovner, created_at, modified_at): 
        self.postId = id
        self.postTitle = str(title)
        self.postContents = str(contents)
        self.postOvner = str(ovner)
        self.postDateCreation = created_at
        self.postDateModification = modified_at
myList.append(post(1,"News about WildLife"," Lorem ispum dolor","Paul",datetime.now(), datetime.now()))
myList.append(post(1,"News about WildLife"," Lorem ispum dolor","Paul",datetime.now(), datetime.now()))

@app.route("/", methods =["GET", "POST"])
def add_post():
    if request.method == "POST":
       # getting input title in HTML form
       post_title = request.form.get("title")
       # getting input owner in HTML form 
       post_owner = request.form.get("owner") 
       # getting input content  in HTML form 
       content = request.form.get("content")
       favMovies = ["Godafther", "Speed", "Goodfellas"]
       myList.append(post(1, post_title, content, post_owner, datetime.now().day, datetime.now()))
    return render_template("add_post.html", myList = myList)

@app.route("/")
def home():
    return render_template("add_post.html")

# New functions
@app.route("/blog/")
def blog():
    return render_template("blog.html")

if __name__ == "__main__":
    app.run(debug = False)
