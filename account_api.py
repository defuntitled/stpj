from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session
from dbremote.user import User, Author
from main import app
import flask
from werkzeug.security import generate_password_hash

login_manager = LoginManager()
login_manager.init_app(app)
session = create_session()

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    global session
    return session.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
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
    return flask.render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect("feed")
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(nickname=form.username.data, email=form.email.data,
                    hashed_password=generate_password_hash(form.password.data))
        # добавить проверку email
        session.add(user)
        session.commit()
        return flask.redirect("/login")
    return flask.render_template('register.html', title='Register', form=form)


@blueprint.route("/register_author")
def new_author():
    author = Author(id=current_user.id, nickname=current_user.nickname, email=current_user.email,
                    hashed_password=current_user.hashed_password)
    user = session.query(User).filter(User.id == current_user.id)
    user.author = True
    session.add(author)
    session.commit()
    return flask.redirect("/dashboard")


@blueprint.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")
