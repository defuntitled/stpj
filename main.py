from dbremote import db_session
from flask import Flask, render_template, redirect
import account_api
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.user import User, Author

app = Flask(__name__)
app.config["SECRET_KEY"] = "sk"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    global session
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/data.sqlite")
    app.register_blueprint(account_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
    return 0


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        return redirect("/feed")
    return render_template("index.html")


if __name__ == "__main__":
    main()
