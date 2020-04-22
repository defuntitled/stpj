from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User, Author
from flask import request
import flask
from werkzeug.security import generate_password_hash

global_init("db/data.sqlite")
session = create_session()

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('ЭЛЕКТРОМЫЛО', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Done!')


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect("/feed")
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(generate_password_hash(form.password.data)):
            login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        return flask.render_template('login.html',
                                     message="Неправильный логин или пароль",
                                     form=form)
    else:
        print(form.errors)
    return flask.render_template('login_template.html', title='Авторизация', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect("/feed")
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.email.data)
        print(form.password.data)
        user = User(nickname=form.username.data, email=form.email.data,
                    hashed_password=generate_password_hash(form.password.data))
        # добавить проверку email
        session.add(user)
        session.commit()
        return flask.redirect("/login")
    return flask.render_template('registration_creator.html', title='Register', form=form)


@blueprint.route("/register_author", methods=['GET', 'POST'])
def new_author():
    form = RegistrationForm()
    if form.validate():
        author = Author(nickname=form.username.data,
                        email=form.email.data,
                        hashed_password=generate_password_hash(form.password.data))
        session.add(author)
        session.commit()
        return flask.redirect("/login")
    else:
        print(form.errors)
    return flask.render_template('registration_creator.html', title='Register', form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")
