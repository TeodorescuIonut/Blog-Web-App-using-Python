from flask import Blueprint, request, jsonify, make_response

from decorators.dependency_injection.injector_di import injector
from decorators.setup.setup import check_setup
from interfaces.post_repository_interface import IPostRepository

api = Blueprint('api', __name__)


@api.route('/api/post/<int:post_id>/')
@injector
@check_setup
def get_json_response(post_repo: IPostRepository, post_id: int):
    post = post_repo.get_by_id(post_id)
    res = make_response(jsonify(res='Post Not Found - 404'), 404)
    if post:
        res = make_response(jsonify(post_id=post.post_id,
                                    owner=post.post_owner,
                                    title=post.post_title,
                                    content=post.post_contents,
                                    creation_date=post.post_date_creation,
                                    image=post.image,
                                    owner_id=post.owner_id
                                    ))
    return res
