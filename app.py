from flask import redirect, url_for
from decorators.setup.setup import check_setup
from decorators.dependency_injection.injector_di import injector
from interfaces.database_upgrade_interface import IDatabaseUpgrade
from main import create_app

app = create_app()


@app.before_first_request
@injector
@check_setup
def db_upgrade(database: IDatabaseUpgrade):
    if database.is_latest_db_version() is False:
        database.upgrade_db()


@app.route('/')
@check_setup
def main():
    return redirect(url_for('post_bp.blog'))


if __name__ == "__main__":
    app.run(port=5000, debug=False)
