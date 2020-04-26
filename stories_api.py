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
    content = StringField("Content", validators=[DataRequired()], )
    send = SubmitField("send")
    like = BooleanField('')
    subscribe = BooleanField("subscribe")


class LikeForm(FlaskForm):
    like = BooleanField('')


class FollowForm(FlaskForm):
    subscribe = SubmitField("subscribe")


@blueprint.route("/feed", methods=["GET", "POST"])  # общая лента с историями
def feed():
    stories_for_watching = []
    session = create_session()
    user = session.query(User).filter(User.id == current_user.id).one()
    if flask.request.method == "POST" and flask.request.form.get('accept'):  # поисковой движок
        results = session.query(Story).filter(Story.head.like(f'%{flask.request.get("search")}%'))
        return flask.render_template("search_result.html", res=results)
    for i in user.followed:
        stories_for_watching += i
    if not stories_for_watching:
        stories_for_watching = session.query(Story).all()
    return flask.render_template("feed.html",
                                 stories=stories_for_watching)


@blueprint.route("/story/<int:sid>", methods=['GET', 'POST'])  # конкретный пост
def story(sid):
    session = create_session()
    story = session.query(Story).filter(Story.id == sid).first()
    if flask.request.method == 'GET':
        content = story.content
        comments = story.commented
        header = story.head
        name = session.query(User).filter(User.id == story.author_id).first()
        can_delete = (current_user.id == story.author_id)

        return flask.render_template("post_template.html", content=content, comments=comments, header=header,
                                     name=name.nickname, likes=story.likes_count, can_delete=can_delete)
    else:
        if not current_user.utype:
            content = story.content
            comments = story.commented
            header = story.head
            name = session.query(User).filter(User.id == story.author_id).first()
            req = flask.request.form
            if req.get('editordata'):
                print('ok')
                comment = Comment()
                comment.content = req.get('editordata')
                comment.head = current_user.nickname
                comment.story = story
                session.commit()
            if req.get('post-like'):
                story.likes_count += 1
                session.commit()
        else:
            req = flask.request.form
            if req.get('post-delete'):
                session.delete(story)
                session.commit()
                return flask.redirect('/dashboard')
    return flask.render_template('post_template.html', content=content, comments=comments, header=header,
                                 name=name.nickname, likes=story.likes_count)

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
