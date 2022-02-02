from turtle import pos
from flask import Flask, flash, redirect, render_template, request, url_for
from models.Post import Post
from datetime import datetime
from PostsRepo.postRepo import postRepo
from operator import attrgetter


myList =postRepo()
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
                myList.create(
                    Post(
                    post_title.title(),
                    content, 
                    post_owner))
                flash("Post added")
                return redirect(url_for('post_bp.blog')) 
                
    return render_template("add_post.html", post = Post, urlPage = add_post)



def blog():
    sortedArray = sorted(myList.posts,key=lambda x: x.postDateCreation,reverse=True)
    return render_template("blog.html", posts = sortedArray, length = len(myList.posts))

def viewPost(postId):
    post = getPostByID(postId)
    return render_template("viewPost.html", post = post)


def deletePost(postId):
    post = myList.getById(postId)
    myList.delete(post)
    flash("Post deleted")
    return redirect(url_for('post_bp.blog'))


def updatePost(postId):
    post = myList.getById(postId)
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
             post.postId = postId
             post.postTitle = post_title
             post.postOwner = post_owner
             post.postContents = content
             post.postDateModification = datetime.now().strftime("%B %d %Y")
             myList.update(post)
             flash("Post updated") 
             return redirect(url_for('post_bp.viewPost',postId = post.postId))
    return render_template("add_post.html", post = post, buttonText = "Update", urlPage = updatePost)

def getPostByID(postId):
    for post in myList.posts:
        if(post.postId == postId):
            return post

def getPostByIndex(postId):
    for post in myList:
        if(post.postId == postId):
            return myList.index(post)
