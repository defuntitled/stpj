from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User, Author
from dbremote.storys import Story, Comment
import flask
from colour import Color
from PIL import ImageDraw, ImageFont, Image
import math

global_init("db/data.sqlite")

blueprint = flask.Blueprint('acman_api', __name__,
                            template_folder='templates')


class ChangeNickname(FlaskForm):
    change = StringField("change", validators=[DataRequired()])
    cub = SubmitField("sub")


class DisFollowed(FlaskForm):
    author = StringField("author", validators=[DataRequired()])
    disfollow = SubmitField("disfollow")


@blueprint.route("/account_page")
def cabinet():
    session = create_session()
    change_nick = ChangeNickname()
    disf = DisFollowed()
    if change_nick.validate_on_submit():
        user = session.query(User).filter(User.id == current_user.id)
        user.nickname = change_nick.change.data
        session.commit()
    if disf.validate_on_submit():
        user = session.query(User).filter(User.id == current_user.id)
        author = session.query(Author).filter(Author.id == disf.author.data)
        user.followed.remove(author)
        session.commit()
    user = session.query(User).filter(User.id == current_user.id)
    


class DStory(FlaskForm):


@blueprint.route("/dashboard")
def dashboard():

