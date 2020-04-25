from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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
        author = session.query(User).filter(User.id == disf.author.data)
        user.followed.remove(author)
        session.commit()
    user = session.query(User).filter(User.id == current_user.id)
    follows = user.followed
    return flask.render_template("account.html", follows=follows)


class DStory(FlaskForm):
    story = StringField("story", validators=[DataRequired()])
    destroy = SubmitField("del")


@blueprint.route("/dashboard")
def dashboard():
    if current_user.utype:
        session = create_session()
        dstory = DStory()
        if dstory.validate_on_submit():
            story = session.query(Story).filter(Story.id == dstory.story.data)
            session.delete(story)
            session.commit()
        change = ChangeNickname()
        if change.validate_on_submit():
            author = session.query(User).filter(User.id == current_user.id)
            author.nickname = change.change.data
            session.commit()
        author = session.query(User).filter(User.id == current_user.id).one()
        stories = author.stories
        followers_count = len(author.followers)
        return flask.render_template("dashboard.html", stories=stories, followers_count=followers_count)
    else:
        return flask.redirect("/")
