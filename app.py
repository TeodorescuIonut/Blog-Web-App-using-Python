from distutils.log import debug
from turtle import pos
from flask import Flask, flash, redirect, render_template, request, url_for
from datetime import datetime
import re
import itertools

app = Flask(__name__)
app.secret_key = "super secret key"

myList = []

class post:
    id = itertools.count()
    def __init__(self, title, contents, owner): 
        self.postId = next(self.id)
        self.postTitle = str(title)
        self.postContents = str(contents)
        self.postOwner = str(owner)
        self.postDateCreation = datetime.now().strftime("%B %d %Y")
        self.postDateModification = ''

@app.route("/PUT/posts", methods =["GET", "POST"])
def add_post():
    if request.method == "POST":
       # getting input title in HTML form
       post_title = request.form.get("title")
       # getting input owner in HTML form 
       post_owner = request.form.get("owner") 
       # getting input content  in HTML form 
       content = request.form.get("content")
       if not post_title:
           flash("Please add a title")
           return redirect(url_for('add_post'))
       elif not post_owner:
           flash("Please add a owner")
           return redirect(url_for('add_post'))
       elif not content:
           flash("Please add content")
           return redirect(url_for('add_post'))
       else:
                myList.append(
                    post(
                    post_title.title(),
                    content, 
                    post_owner))
       return redirect(url_for('blog')) 
    return render_template("add_post.html", post = post, urlPage = add_post)


# New functions
@app.route("/")
def blog():

    return render_template("blog.html", posts = myList, length = len(myList))

@app.route("/GET/<int:postId>")
def viewPost(postId):
    post = getPostByID(postId)
    return render_template("viewPost.html", post = post)

@app.route("/DELETE/<int:postId>")
def deletePost(postId):
    post = getPostByID(postId)
    myList.remove(post)
    flash("Post deleted")
    return redirect(url_for('blog'))

@app.route("/UPDATE/<int:postId>", methods =["GET", "POST"])
def updatePost(postId):
    post = getPostByID(postId)
    if request.method == "POST":      
       postIndex = getPostByIndex(postId)
            # getting input title in HTML form
       post_title = request.form.get("title")
       # getting input owner in HTML form 
       post_owner = request.form.get("owner") 
       # getting input content  in HTML form 
       content = request.form.get("content")
       postDateCreation = post.postDateCreation
       if not post_title:
           flash("Please add a title")
           return redirect(url_for('add_post'))
       elif not post_owner:
           flash("Please add a owner")
           return redirect(url_for('add_post'))
       elif not content:
           flash("Please add content")
           return redirect(url_for('add_post'))
       else:
                myList[postIndex].postTitle = post_title.title()
                myList[postIndex].postOwner = post_owner
                myList[postIndex].postContents = content
                myList[postIndex].postDateCreation = postDateCreation
                myList[postIndex].postDateModification = datetime.now().strftime("%B %d %Y")
       flash("Post updated") 
       return redirect(url_for('blog'))
    return render_template("add_post.html", post = post, buttonText = "Update", urlPage = updatePost)

def getPostByID(postId):
    for post in myList:
        if(post.postId == postId):
            return post

def getPostByIndex(postId):
    for post in myList:
        if(post.postId == postId):
            return myList.index(post)

if __name__ == "__main__":
    app.run(debug = True)
