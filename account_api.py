from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User, Author
from dbremote.storys import Story


from flask import request

from main import app
import os

import flask
from werkzeug.security import generate_password_hash

global_init("db/data.sqlite")
session = create_session()

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


class LoginForm(FlaskForm):
    email = StringField('ЭЛЕКТРОМЫЛО', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('ЭЛЕКТРОМЫЛО', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Done!')

    def validate_username(self, username):
        session = create_session()
        user = session.query(User).filter_by(nickname=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        session = create_session()
        user = session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect("/feed")
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        print(generate_password_hash(form.password.data))
        return flask.render_template('login_template.html',
                                     message="Неправильный логин или пароль",
                                     form=form)
    else:
        print(form.errors)
    return flask.render_template('login_template.html', action=2, title='Авторизация', form=form)


@blueprint.route("/login_author", methods=["GET", "POST"])
def login_author():
    if current_user.is_authenticated:
        return flask.redirect("/dashboard")
    form = LoginForm()
    if form.validate_on_submit():
        author = session.query(Author).filter(Author.email == form.email.data).first()
        if author and author.check_password(form.password.data):
            login_user(author, remember=form.remember_me.data)
            return flask.redirect("/dashboard")
        return flask.render_template('login_template.html',
                                     form=form)
    else:
        print(form.errors)
    return flask.render_template('login_template.html', action=1, form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect("/feed")
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.email.data)
        print(form.password.data)
        user = User()
        user.nickname = form.username.data
        user.email = form.email.data
        user.hashed_password = generate_password_hash(form.password.data)

        # добавить проверку email
        session = create_session()
        session.add(user)
        print(type(form.username.data), type(form.email.data),
              type(generate_password_hash(form.password.data)))
        session.commit()
        return flask.redirect("/login")
    return flask.render_template('registration_creator.html', action=2, title='Register', form=form)


@blueprint.route("/register_author", methods=['GET', 'POST'])
def new_author():
    form = RegistrationForm()
    if form.validate():
        author = Author()
        author.nickname = form.username.data
        author.email = form.email.data
        author.hashed_password = generate_password_hash(form.password.data)
        session = create_session()
        session.add(author)
        session.commit()
        os.mkdir(f"data/{author.id}")
        return flask.redirect("/login")
    else:
        print(form.errors)
    return flask.render_template('registration_creator.html', action=1, form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")


@blueprint.route("/alpha-beta", methods=['GET', 'POST'])
def kek():
    if request.method == 'GET':
        print(type(current_user))
        return flask.render_template('create_post.html', user=current_user)
    else:
        story = Story()
        story.content = request.form.get('editordata')
        session.add(story)
        session.commit()
        os.mkdir(f"data/{author.id}")
        return flask.redirect("/login")
        print(request.form.get('editordata'))
        return 'ok'
