from datetime import datetime
from services.post_factory import PostFactory
from flask import current_app, flash, redirect, render_template, request, url_for
from models.post import Post

repo = PostFactory.create('PostDbRepo')
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
            new_post =  Post(
                post_title.title(),
                content,
                post_owner)
            repo.create(new_post)
            flash("Post added")
            return redirect(url_for('post_bp.view_post',post_id = new_post.post_id))
    return render_template("add_post.html", post = Post, urlPage = add_post)

def blog():
    sorted_array = sorted(repo.get_previews(),key=lambda x: x.post_date_creation,reverse=True)
    return render_template("blog.html", posts = sorted_array, length = len(repo.posts))

def view_post(post_id):
    post = repo.get_by_id(post_id)
    return render_template("viewPost.html", post = post)


def delete_post( post_id):
    post = repo.get_by_id(post_id)
    repo.delete(post)
    flash("Post deleted")
    return redirect(url_for('post_bp.blog'))


def update_post(post_id):
    post = repo.get_by_id(post_id)
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
            return render_template("add_post.html",
            post = post, buttonText = "Update",
            urlPage = update_post)
        else:
            post.post_id = post_id
            post.post_title = post_title
            post.post_owner = post_owner
            post.post_contents = content
            post.post_date_modification = datetime.now().strftime("%B %d %Y")
            repo.update(post)
            flash("Post updated")
            return redirect(url_for('post_bp.view_post',post_id = post.post_id))
    return render_template("add_post.html",
        post = post, buttonText = "Update",
        urlPage = update_post)

def get_post_by_id(post_id):
    for post in repo.posts:
        if post.post_id == post_id :
            return post
            