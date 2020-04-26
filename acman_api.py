from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User
from dbremote.storys import Story, Comment
import flask
import os

global_init("db/data.sqlite")

blueprint = flask.Blueprint('acman_api', __name__,
                            template_folder='templates')


class ChangeNickname(FlaskForm):
    change = StringField("change", validators=[DataRequired()])
    cub = SubmitField("sub")


class FollowForm(FlaskForm):
    subscribe = SubmitField("subscribe")


class DisFollowed(FlaskForm):
    author = StringField("author", validators=[DataRequired()])
    disfollow = SubmitField("disfollow")


class DStory(FlaskForm):
    story = IntegerField("story", validators=[DataRequired()])
    destroy = SubmitField("Delete story")


@blueprint.route("/account_page", methods=["GET", "POST"])
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
        author = session.query(User).filter(User.id == disf.author.data)
        user.followed.remove(author)
        session.commit()
    user = session.query(User).filter(User.id == current_user.id).first()
    follows = user.followed
    name = user.nickname
    return flask.render_template("account.html", follows=follows, name=name)


@blueprint.route("/dashboard", methods=["GET", "POST"])  # панель управления постами и авторской статистикой
def dashboard():
    session = create_session()
    author = session.query(User).filter(User.id == current_user.id).first()
    stories = author.stories
    followers_count = author.followers
    return flask.render_template("dashboard.html", stories=stories, followers=followers_count)


@blueprint.route("/author/<int:aid>", methods=["GET", "POST"])  # "визитная карточка" автора
def card(aid):
    session = create_session()
    author = session.query(User).filter(User.id == aid).first()
    user = session.query(User).filter(User.id == current_user.id).first()
    if flask.request.method == 'GET':
        if not current_user.is_authenticated:
            return flask.redirect("/")
        subscribed = author in user.followed
        return flask.render_template("card.html", name=author.nickname, fc=author.followers, sub=subscribed)
    else:
        req = flask.request.form
        if req.get('subscribe-button'):
            subscribed = author in user.followed
            req = flask.request.form
            if req.get('subscribe-button'):

                if author in user.followed:
                    user.followed.remove(author)
                    session.commit()
                    author.followers -= 1
                    session.commit()
                else:
                    user.followed.append(author)
                    session.commit()
                    author.followers += 1
                    session.commit()
        return flask.redirect('/feed')

        return flask.render_template("card.html", name=author.nickname, fc=author.followers, sub=subscribed)
