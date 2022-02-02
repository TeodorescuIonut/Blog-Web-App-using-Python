from flask import Blueprint
from controllers.PostController import add_post, blog, viewPost, updatePost, deletePost
post_bp = Blueprint('post_bp', __name__)

post_bp.route('/')(blog)
post_bp.route('/POST/CREATE/posts', methods =["GET", "POST"])(add_post)
post_bp.route('/POST/VIEW/<int:postId>')(viewPost)
post_bp.route('/POST/UPDATE/<int:postId>', methods =["GET", "POST"])(updatePost)
post_bp.route('/POST/DELETE/<int:postId>')(deletePost)