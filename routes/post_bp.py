from datetime import datetime
from functools import wraps
from databases.database_config import DatabaseConfig
from decorators.decorators import check_setup, injector
from flask import Blueprint, flash, render_template, request, redirect, url_for
from models.post import Post
from interfaces.post_repository_interface import IPostRepository

@injector
class PostBlueprint:
    
    def __init__(self,repo:IPostRepository):
        self.post_bp = Blueprint('post_bp',__name__)
        self.repo = repo

    def create(self):       
        self.post_bp.route('/')(self.blog)
        self.post_bp.route('/POST')(self.blog)
        self.post_bp.route('/CREATE/posts', methods =["GET", "POST"])(self.add_post)
        self.post_bp.route('/VIEW/<int:post_id>')(self.view_post)
        self.post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])(self.update_post)
        self.post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])(self.delete_post)
        return self.post_bp
  
    @check_setup
    def blog(self):
        return render_template("blog.html", posts = self.repo.get_all(), length = len(self.repo.posts))
    @check_setup
    def add_post(self):
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
                return render_template("add_post.html", post = post, urlPage = self.add_post)
            else:
                new_post =  Post(
                    post_title.title(),
                    content,
                    post_owner)
            self.repo.create(new_post)
            flash("Post added")
            return redirect(url_for('post_bp.view_post',post_id = new_post.post_id))
        return render_template("add_post.html", post = Post, urlPage = self.add_post)

    @check_setup
    def view_post(self,post_id):
            post = self.repo.get_by_id(post_id)
            return render_template("viewPost.html", post = post)

    @check_setup
    def update_post(self,post_id):
        post = self.repo.get_by_id(post_id)
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
                    urlPage = staticmethod(self.update_post))
            else:
                post.post_id = post_id
                post.post_title = post_title
                post.post_owner = post_owner
                post.post_contents = content
                post.post_date_modification = datetime.now().strftime("%B %d %Y")
                self.repo.update(post)
                flash("Post updated")
            return redirect(url_for('post_bp.view_post',post_id = post.post_id))
        return render_template("add_post.html",
                post = post, buttonText = "Update",
                urlPage = self.update_post)
    @check_setup
    def delete_post(self,post_id):
        post = self.repo.get_by_id(post_id)
        self.repo.delete(post)
        flash("Post deleted")
        return redirect(url_for('post_bp.blog'))