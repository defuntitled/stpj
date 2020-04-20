from dbremote import db_session
from flask import Flask, render_template
import rsa

app = Flask(__name__)
app.config["SECRET_KEY"] = "sk"
api = Api(app)


def main():
    db_session.global_init("db/data.sqlite")
    return 0


@app.route("/")
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    main()
