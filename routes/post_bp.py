from flask import Blueprint
from controllers.post_controller import add_post, blog, view_post, update_post, delete_post
post_bp = Blueprint('post_bp', __name__)

post_bp.route('/')(blog)
post_bp.route('/CREATE/posts', methods =["GET", "POST"])(add_post)
post_bp.route('/VIEW/<int:post_id>', methods =["GET", "POST"])(view_post)
post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])(update_post)
post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])(delete_post)
