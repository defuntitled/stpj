from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User, Author
from main import app
import flask
from werkzeug.security import generate_password_hash

global_init("db/data.sqlite")
session = create_session()

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


class CommentForm(FlaskForm):
    content = StringField("Content",validators=[DataRequired()])


