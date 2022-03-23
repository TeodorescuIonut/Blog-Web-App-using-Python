from datetime import datetime
from decorators.setup.setup import check_setup
from decorators.dependency_injection.injector_di import injector
from decorators.authentification.sing_in_required import sign_in_required
from flask import Blueprint, flash, render_template, request, redirect, url_for
from interfaces.authentication_interface import IAuthentication
from models.post import Post
from interfaces.post_repository_interface import IPostRepository
from models.user import User

@injector
class PostBlueprint:
    repo:IPostRepository
    auth:IAuthentication
    def __init__(self,repo:IPostRepository, authentication:IAuthentication):   
        self.repo = repo
        self.post_bp = Blueprint('post_bp',__name__)
        self.auth = authentication

    def create(self):       
        self.post_bp.route('/')(self.blog)
        self.post_bp.route('/POST')(self.blog)
        self.post_bp.route('/CREATE/posts', methods =["GET", "POST"])(self.add_post)
        self.post_bp.route('/VIEW/<int:post_id>')(self.view_post)
        self.post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])(self.update_post)
        self.post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])(self.delete_post)
        self.post_bp.context_processor(self.context_processor)
        return self.post_bp
    @check_setup
    def context_processor(self):
        if self.auth.is_logged_in():
            user= self.auth.get_user_details()
        else:
            user = None
        return dict(logged_user = user,logged_in = self.auth.is_logged_in())

    @check_setup
    def blog(self):
        return render_template("blog.html",posts = self.repo.get_all(), length = len(self.repo.posts))
    
    @check_setup
    @sign_in_required
    def add_post(self):
        owner:User = self.auth.get_user_details()
        if request.method == "POST":
            # getting input title in HTML form
            post_title = request.form.get("title")
            # getting input content  in HTML form
            content = request.form.get("content")
            post = Post(owner.user_name,post_title, content,owner.user_id)
            error = None
            if not post_title:
                error = "Please add a title"
            elif not content:
                error = "Please add content"
            if error:
                flash(error)
                return render_template("add_post.html", post = post, urlPage = self.add_post)
            else:
                new_post =  Post(
                    owner.user_name,
                    post_title.title(),
                    content,
                    owner.user_id)
            self.repo.create(new_post)
            flash("Post added")
            return redirect(url_for('post_bp.view_post',post_id = new_post.post_id))
        return render_template("add_post.html", post = Post, urlPage = self.add_post)

    @check_setup
    def view_post(self,post_id):
        post = self.repo.get_by_id(post_id)
        return render_template("viewPost.html", post = post)

    @check_setup
    @sign_in_required
    def update_post(self,post_id):
        post:Post = self.repo.get_by_id(post_id)
        if request.method == "POST":
            # getting input title in HTML form
            post_title = request.form.get("title")
            # getting input content  in HTML form
            content = request.form.get("content")
            error = None
            if not post_title:
                error = "Please add a title"
            elif not content:
                error = "Please add content"
            if error:
                flash(error)
                return render_template("add_post.html",
                post = post, buttonText = "Update",
                urlPage = self.update_post)
            else:
                post.post_id = post_id
                post.post_title = post_title
                post.post_contents = content
                post.post_date_modification = datetime.now().strftime("%B %d %Y")
                self.repo.update(post)
                flash("Post updated")
                return render_template('viewPost.html',post_id = post.post_id, post = post)
        return render_template("add_post.html",post = post, buttonText = "Update")

    @check_setup
    @sign_in_required
    def delete_post(self,post_id):
        post = self.repo.get_by_id(post_id)
        self.repo.delete(post)
        flash("Post deleted")
        return redirect(url_for('post_bp.blog'))