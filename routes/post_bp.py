from flask import Blueprint
from controllers.PostController import add_post, blog, viewPost, updatePost, deletePost
post_bp = Blueprint('post_bp', __name__)

post_bp.route('/')(blog)
post_bp.route('/CREATE/posts', methods =["GET", "POST"])(add_post)
post_bp.route('/VIEW/<int:postId>', methods =["GET", "POST"])(viewPost)
post_bp.route('/UPDATE/<int:postId>', methods =["GET", "POST"])(updatePost)
post_bp.route('/DELETE/<int:postId>', methods =["GET", "POST"])(deletePost)