from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for, current_app
from models.post import Post


def construct_bp(repo):
    post_bp = Blueprint('post_bp', __name__)
    @post_bp.route('/')
    def blog():
        return render_template("blog.html", posts = repo.get_all(), length = len(repo.posts))
    @post_bp.route('/CREATE/posts', methods =["GET", "POST"])
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

    @post_bp.route('/VIEW/<int:post_id>', methods =["GET", "POST"])
    def view_post(post_id):
        post = repo.get_by_id(post_id)
        return render_template("viewPost.html", post = post)

    @post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])
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
    @post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])
    def delete_post( post_id):
        post = repo.get_by_id(post_id)
        repo.delete(post)
        flash("Post deleted")
        return redirect(url_for('post_bp.blog'))
    return post_bp