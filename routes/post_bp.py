from flask import Blueprint, current_app
import sys
import os
from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from controllers.post_controller import blog,add_post, delete_post, view_post, update_post
post_bp = Blueprint('post_bp', __name__)


post_bp.route('/')(blog)
post_bp.route('/CREATE/posts', methods =["GET", "POST"])(add_post)
post_bp.route('/VIEW/<int:post_id>', methods =["GET", "POST"])(view_post)
post_bp.route('/UPDATE/<int:post_id>', methods =["GET", "POST"])(update_post)
post_bp.route('/DELETE/<int:post_id>', methods =["GET", "POST"])(delete_post)
