from turtle import pos
from flask import Flask, flash, redirect, render_template, request, url_for
from models.Post import Post
from datetime import datetime


myList =[]
def add_post():
    if request.method == "POST":
       # getting input title in HTML form
       post_title = request.form.get("title")
       # getting input owner in HTML form 
       post_owner = request.form.get("owner") 
       # getting input content  in HTML form 
       content = request.form.get("content")
       post = Post(post_title, content, post_owner)
       error = None
       if not post_title:
           error = "Please add a title"   
       elif not post_owner:
           error = "Please add a owner"
       elif not content:
           error = "Please add content"
       if error:
           flash(error)
           return render_template("add_post.html", post = post, urlPage = add_post)
       else:
                myList.append(
                    Post(
                    post_title.title(),
                    content, 
                    post_owner))
                flash("Post added")
                return redirect(url_for('post_bp.blog')) 
                
    return render_template("add_post.html", post = Post, urlPage = add_post)



def blog():
    return render_template("blog.html", posts = myList, length = len(myList))


def viewPost(postId):
    post = getPostByID(postId)
    return render_template("viewPost.html", post = post)


def deletePost(postId):
    post = getPostByID(postId)
    myList.remove(post)
    flash("Post deleted")
    return redirect(url_for('post_bp.blog'))


def updatePost(postId):
    post = getPostByID(postId)
    postIndex = getPostByIndex(postId)
    if request.method == "POST":      
            # getting input title in HTML form
       post_title = request.form.get("title")
       # getting input owner in HTML form 
       post_owner = request.form.get("owner") 
       # getting input content  in HTML form 
       content = request.form.get("content")
       error = None
       if not post_title:
           error = "Please add a title"   
       elif not post_owner:
           error = "Please add a owner"
       elif not content:
           error = "Please add content"
       if error:
           flash(error)
           return render_template("add_post.html", post = post, buttonText = "Update", urlPage = updatePost)
       else:
             myList[postIndex].postTitle = post_title.title()
             myList[postIndex].postOwner = post_owner
             myList[postIndex].postContents = content
             myList[postIndex].postDateCreation = post.postDateCreation
             myList[postIndex].postDateModification = datetime.now().strftime("%B %d %Y")
             flash("Post updated") 
             return redirect(url_for('post_bp.blog'))
    return render_template("add_post.html", post = post, buttonText = "Update", urlPage = updatePost)

def getPostByID(postId):
    for post in myList:
        if(post.postId == postId):
            return post

def getPostByIndex(postId):
    for post in myList:
        if(post.postId == postId):
            return myList.index(post)
