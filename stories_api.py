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

blueprint = flask.Blueprint('news_api2', __name__,
                            template_folder='templates')


class CommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()])
    send = SubmitField("send")


class LikeForm(FlaskForm):
    like = SubmitField("like")


class FollowForm(FlaskForm):
    subscribe = SubmitField("subscribe")


@blueprint.route("/feed", methods=["GET", "POST"])
def feed():
    stories_for_watching = []
    session = create_session()
    user = session.query(User).filter(User.id == current_user.id)
    for i in user.followed:
        stories_for_watching += i
    return flask.render_template("feed.html",
                                 stories=stories_for_watching)


@blueprint.route("/story/<int:sid>")
def story(sid):
    session = create_session()
    story = session.query(Story).filter(Story.id == sid)
    sub = FollowForm()
    form = CommentForm()
    like = LikeForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.content = form.content.data
        comment.head = current_user.nickname
        session.add(comment)
        session.commit()
    if like.validate_on_submit():
        story.likes_count += 1
        session.commit()
    if sub.validate_on_submit():
        user = session.query(User).filter(User.id == current_user.id, story.author in User.followed)
        if user:
            user.followed.remove(story.author)
            session.commit()
        else:
            user.followed.append(story.author)
            session.commit()
    content = story.content
    comments = story.commented
    return flask.render_template("story.html", content=content, comments=comments)


def generate_cover(sid, aid, grad):
    img = Image.new("RGBA", (1920, 1080))
    im = img.load()
    if grad == 0:
        col = Color((157, 0, 185))
        colors = list(map(lambda x: x.rgb, col.range_to(Color("blue"), 1920)))
    elif grad == 1:
        col = Color((157, 0, 185))
        colors = list(map(lambda x: x.rgb, col.range_to(Color("white"), 1920)))
    elif grad == 2:
        col = Color((157, 0, 185))
        colors = list(map(lambda x: x.rgb, col.range_to(Color((74, 186, 87)), 1920)))
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            im[i, j] = colors[i]

    im.save(f"data/{aid}/{sid}_cover.png")


@blueprint.route("/post", methods=['GET', 'POST'])
def post():
    if flask.request.method == 'GET':
        return flask.render_template('create_post.html')
    else:
        text = flask.request.form.get('editordata')
        post_name = flask.request.form.get('post-name')

        post = Story()
        post.content = text
        post.head = post_name
        return text
