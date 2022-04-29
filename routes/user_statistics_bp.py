from flask import Blueprint, render_template

from decorators.authorization.check_if_admin import check_if_admin
from decorators.dependency_injection.injector_di import injector
from decorators.setup.setup import check_setup
from interfaces.authentication_interface import IAuthentication
from interfaces.user_statistics_interface import IUserStatistics

user_statistics = Blueprint('user_statistics', __name__, url_prefix='/statistics')


@user_statistics.route("/")
@injector
@check_setup
@check_if_admin
def statistics(auth: IAuthentication, data_statistics: IUserStatistics):
    if auth.is_logged_in():
        user = auth.get_user_details()
    else:
        user = None
    users = data_statistics.get_statistics()
    return render_template("statistics.html", users=users,
                           logged_user=user, logged_in=auth.is_logged_in())
