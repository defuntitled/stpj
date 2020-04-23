from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User, Author
from dbremote.storys import Story, Comment
from main import app
import flask
from werkzeug.security import generate_password_hash

global_init("db/data.sqlite")

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


class CommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()])
    send = SubmitField("send")


@blueprint.route("/feed", methods=["GET", "POST"])
def feed():
    stories_for_watching = []
    session = create_session()
    user = session.query(User).filter(User.id == current_user.id)
    for i in user.followed:
        stories_for_watching += i
    return flask.render_template("feed.html",
                                 stories=stories_for_watching)  # в шаблоне циклом надо идти по этой хуйне


@blueprint.route("/story/<sid:int>")
def story(sid):
    session = create_session()
    story = session.query(Story).filter(Story.id == sid)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.content = form.content.data
        comment.head = current_user.nickname
        session.add(comment)
        session.commit()
    content = story.content
    comments = story.commented
    return flask.render_template("story.html",content=content,comments=comments)



