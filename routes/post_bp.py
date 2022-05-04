from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for
from decorators.authorization.check_if_post_owner_or_admin import check_if_post_owner_or_admin
from decorators.authorization.check_post_exists import check_post_exists
from decorators.setup.setup import check_setup
from decorators.dependency_injection.injector_di import injector
from decorators.authentification.sing_in_required import sign_in_required
from interfaces.authentication_interface import IAuthentication
from interfaces.filtering_interface import IFiltering
from interfaces.pagination_interface import IPagination
from interfaces.post_repository_interface import IPostRepository
from models.post import Post
from models.user import User


@injector
class PostBlueprint:
    repo: IPostRepository
    auth: IAuthentication
    pagination: IPagination
    filtering: IFiltering

    def __init__(self, repo: IPostRepository,
                 authentication: IAuthentication,
                 pagination: IPagination,
                 filtering: IFiltering
                 ):
        self.repo = repo
        self.post_bp = Blueprint('post_bp', __name__)
        self.auth = authentication
        self.pagination = pagination
        self.filtering = filtering

    def create(self):
        self.post_bp.route('/', methods=["GET", "POST"])(self.blog)
        self.post_bp.route('/POST', methods=["GET", "POST"])(self.blog)
        self.post_bp.route('/CREATE/posts', methods=["GET", "POST"])(self.add_post)
        self.post_bp.route('/VIEW/<int:post_id>')(self.view_post)
        self.post_bp.route('/api/post/<int:post_id>')(self.api_post)
        self.post_bp.route('/UPDATE/<int:post_id>', methods=["GET", "POST"])(self.update_post)
        self.post_bp.route('/DELETE/<int:post_id>', methods=["GET", "POST"])(self.delete_post)
        self.post_bp.context_processor(self.context_processor)
        return self.post_bp

    @check_setup
    def context_processor(self):
        selected_user_id = self.filtering.get_owner_id()
        selected_user = ""
        if selected_user_id != -1:
            selected_user = self.filtering.repo.get_by_id(selected_user_id).user_name
        if self.auth.is_logged_in():
            user = self.auth.get_user_details()
        else:
            user = None
        return dict(logged_user=user, logged_in=self.auth.is_logged_in(),
                    selected_user_id=selected_user_id, selected_user=selected_user)

    @check_setup
    def blog(self):
        if request.method == "POST":
            posts_per_page = request.form.get("input_no_of_posts")
            if posts_per_page is None:
                flash('Please add a valid option')
                return redirect(url_for('post_bp.blog'))
            self.pagination.set_no_per_page(int(posts_per_page))
        filtering = self.filtering.return_filter()
        posts = self.repo.get_all(self.pagination.no_per_page,
                                  self.pagination.offset(),
                                  filtering.selected_owner_id)
        no_of_posts = self.repo.no_posts
        posts_pagination = self.pagination.set_pagination(no_of_posts)
        return render_template("blog.html", posts=posts,
                               pagination=posts_pagination,
                               filter=filtering, length=len(posts))

    @check_setup
    @sign_in_required
    def add_post(self):
        owner: User = self.auth.get_user_details()
        if request.method == "POST":
            # getting input title in HTML form
            post_title = request.form.get("title")
            # getting input content  in HTML form
            content = request.form.get("content")
            post = Post(owner.user_name, post_title, content, owner.user_id)
            if 'image' not in request.files:
                image_file = None
            else:
                image_file = request.files['image']
            error = None
            if not post_title:
                error = "Please add a title"
            elif not content:
                error = "Please add content"
            if error:
                flash(error)
                return render_template("add_post.html", post=post, urlPage=self.add_post)
            else:
                new_post = Post(
                    owner.user_name,
                    post_title.title(),
                    content,
                    owner.user_id,
                    image_file
                )
            self.repo.create(new_post, image_file)
            flash("Post added")
            return redirect(url_for('post_bp.view_post', post_id=new_post.id))
        return render_template("add_post.html", post=Post, urlPage=self.add_post)

    @check_setup
    @check_post_exists
    def view_post(self, post_id):
        post = self.repo.get_by_id(post_id)
        return render_template("viewPost.html", post=post)

    @check_setup
    @check_post_exists
    def api_post(self, post_id):
        return render_template("post_api.html", post_id=post_id)

    @check_setup
    @check_post_exists
    @sign_in_required
    @check_if_post_owner_or_admin
    def update_post(self, post_id):
        post: Post = self.repo.get_by_id(post_id)
        if request.method == "POST":
            # getting input title in HTML form
            post_title = request.form.get("title")
            # getting input content  in HTML form
            content = request.form.get("content")
            if 'image' not in request.files:
                image_file = None
            else:
                image_file = request.files['image']
            error = None
            if not post_title:
                error = "Please add a title"
            elif not content:
                error = "Please add content"
            if error:
                flash(error)
                return render_template("add_post.html",
                                       post=post, buttonText="Update",
                                       urlPage=self.update_post)
            else:
                post.id = post_id
                post.title = post_title
                post.contents = content
                post.modified_at = datetime.now().strftime("%B %d %Y")
                post.image = post.image
                self.repo.update(post, image_file)
                flash("Post updated")
                return render_template('viewPost.html', post_id=post.id, post=post)
        return render_template("add_post.html", post=post, buttonText="Update")

    @check_setup
    @check_post_exists
    @sign_in_required
    @check_if_post_owner_or_admin
    def delete_post(self, post_id):
        post = self.repo.get_by_id(post_id)
        self.repo.delete(post)
        flash("Post deleted")
        return redirect(url_for('post_bp.blog'))
