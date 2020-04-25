from dbremote import db_session
from flask import Flask, render_template, redirect
import flask
import account_api
import acman_api
import stories_api
import acman_api
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "sk"
UPLOAD_FOLDER = '/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/data.sqlite")
    app.register_blueprint(account_api.blueprint)
    app.register_blueprint(stories_api.blueprint)
    app.register_blueprint(acman_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
    return 0


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        return redirect("/feed")
    return render_template("index.html")


@app.errorhandler(404)
def not_found_error(err):
    return render_template('error_handler.html'), 404


@app.errorhandler(500)
def not_found_error(err):
    return render_template('error_handler.html'), 500


if __name__ == "__main__":
    main()
