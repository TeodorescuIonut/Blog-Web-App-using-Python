from flask import Blueprint
from services.post_db_repo import PostDbRepo
from services.post_repo import PostRepo
from controllers.post_controller import PostController
post_bp = Blueprint('post_bp', __name__)

repo_memory = PostRepo.create_repo()
post_controller = PostController(repo_memory)


post_bp.route('/')(post_controller.blog)
post_bp.route('/CREATE/posts', methods =["GET", "POST"])(post_controller.add_post)
post_bp.route('/VIEW/<int:post_id>', methods =["GET", "POST"])(post_controller.view_post)
post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])(post_controller.update_post)
post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])(post_controller.delete_post)
