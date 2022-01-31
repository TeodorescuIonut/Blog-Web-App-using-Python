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
       if not post_title:
           flash("Please add a title")
           return redirect(url_for('post_bp.add_post'))
       elif not post_owner:
           flash("Please add a owner")
           return redirect(url_for('post_bp.add_post'))
       elif not content:
           flash("Please add content")
           return redirect(url_for('post_bp.add_post'))
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
           return redirect(url_for('post_bp.add_post'))
       elif not post_owner:
           flash("Please add a owner")
       elif not content:
           flash("Please add content")
       else:
             myList[postIndex].postTitle = post_title.title()
             myList[postIndex].postOwner = post_owner
             myList[postIndex].postContents = content
             myList[postIndex].postDateCreation = postDateCreation
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
