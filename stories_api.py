from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User
from dbremote.storys import Story, Comment
import flask

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


@blueprint.route("/feed", methods=["GET", "POST"])  # общая лента с историями
def feed():
    stories_for_watching = []
    session = create_session()
    user = session.query(User).filter(User.id == current_user.id).one()

    for i in user.followed:
        stories_for_watching += i
    if not stories_for_watching:
        stories_for_watching = session.query(Story).all()
    return flask.render_template("feed.html",
                                 stories=stories_for_watching)


@blueprint.route("/story/<int:sid>")  # конкретный пост
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
        comment.story = story
        session.add(comment)
        session.commit()
    if like.validate_on_submit():
        story.likes_count += 1
        session.commit()
    if sub.validate_on_submit():
        user = session.query(User).filter(User.id == current_user.id)
        if story.author in user.followed:
            user.followed.remove(story.author)
            session.commit()
            author = session.query(User).filter(User.id == story.authror.id)
            author.followers -= 1
            session.commit()
        else:
            user.followed.append(story.author)
            session.commit()
            author = session.query(User).filter(User.id == story.authror.id)
            author.followers += 1
            session.commit()
    content = story.content
    comments = story.commented

    return flask.render_template("story.html", content=content, comments=comments)


@blueprint.route("/post", methods=['GET', 'POST'])  # создание истории
def post():
    if current_user.is_authenticated:
        if flask.request.method == 'GET':
            return flask.render_template('create_post.html')
        else:
            text = flask.request.form.get('editordata')
            post_name = flask.request.form.get('post-name')
            checkbox1 = flask.request.form.get('radio1')
            checkbox2 = flask.request.form.get('radio2')
            checkbox3 = flask.request.form.get('radio3')
            if checkbox1:
                color = "/static/img/white.jpg"
            elif checkbox2:
                color = "/static/img/red.jpg"
            elif checkbox3:
                color = "/static/img/green.jpg"
            else:
                color = "/static/img/white.jpg"
            print(text)
            print(post_name)
            print(checkbox1)
            print(checkbox2)
            print(checkbox3)

            post = Story()
            post.content = text
            post.head = post_name
            post.author_id = current_user.id
            post.cover = color
            session = create_session()
            session.add(post)
            session.commit()
            return flask.redirect("/dashboard")
    else:
        return flask.redirect('/')
