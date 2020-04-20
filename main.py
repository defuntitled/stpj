from dbremote import db_session
from flask import Flask
from flask_restful import Api
import rsa

app = Flask(__name__)
app.config["SECRET_KEY"] = "sk"
api = Api(app)


def main():
    db_session.global_init("db/data.sqlite")
    return 0


if __name__ == "__main__":
    main()
