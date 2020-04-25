from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_login import LoginManager, login_user, logout_user, current_user
from dbremote.db_session import create_session, global_init
from dbremote.user import User
import os
from main import app
import flask
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

global_init("db/data.sqlite")

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg'}


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
    ava = FileField("avatar")
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route("/login/<string:par>", methods=["GET", "POST"])
def login(par):
    if par == "user":
        res = flask.make_response("Setting a cookie")
        res.set_cookie('utype', 'user', max_age=60 * 60 * 24 * 365 * 2)
        if current_user.is_authenticated:
            return flask.redirect("/feed")
        form = LoginForm()
        if form.validate_on_submit():
            session = create_session()
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
        return flask.render_template('login_template.html', action=False, title='Авторизация',
                                     form=form)
    elif par == "author":
        res = flask.make_response("Setting a cookie")
        res.set_cookie('utype', 'author', max_age=60 * 60 * 24 * 365 * 2)
        if current_user.is_authenticated:
            return flask.redirect("/dashboard")
        form = LoginForm()
        if form.validate_on_submit():
            session = create_session()
            author = session.query(User).filter(User.email == form.email.data).first()
            if author and author.check_password(form.password.data):
                login_user(author, remember=form.remember_me.data)
                return flask.redirect("/dashboard")
            return flask.render_template('login_template.html',
                                         form=form)
        else:
            print(form.errors)
        return flask.render_template('login_template.html', action=True, form=form)


# @blueprint.route("/login_author", methods=["GET", "POST"])
# def login_author():
#     if current_user.is_authenticated:
#         return flask.redirect("/dashboard")
#     form = LoginForm()
#     if form.validate_on_submit():
#         author = session.query(Author).filter(Author.email == form.email.data).first()
#         if author and author.check_password(form.password.data):
#             login_user(author, remember=form.remember_me.data)
#             return flask.redirect("/dashboard")
#         return flask.render_template('login_template.html',
#                                      form=form)
#     else:
#         print(form.errors)
#     return flask.render_template('login_template.html', action=1, form=form)


@blueprint.route('/register/<string:par>', methods=['GET', 'POST'])
def register(par):
    if par == "user":
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
            if allowed_file(form.ava.file.filename):
                file_name = secure_filename(form.ava.file.filename)
                form.ava.file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                user.avatar = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            session = create_session()
            session.add(user)
            print(type(form.username.data), type(form.email.data),
                  type(generate_password_hash(form.password.data)))
            session.commit()

            return flask.redirect("/login/user")
        return flask.render_template('registration_creator.html', action=False, title='Register',
                                     form=form)
    elif par == "author":
        form = RegistrationForm()
        if form.validate():
            author = User()
            author.nickname = form.username.data
            author.email = form.email.data
            author.hashed_password = generate_password_hash(form.password.data)
            author.utype = True
            if allowed_file(form.ava.file.filename):
                file_name = secure_filename(form.ava.file.filename)
                form.ava.file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                author.avatar = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            session = create_session()
            session.add(author)
            session.commit()

            return flask.redirect("/login/author")
        else:
            print(form.errors)
        return flask.render_template('registration_creator.html', action=True, form=form)


# @blueprint.route("/register_author", methods=['GET', 'POST'])
# def new_author():
#     form = RegistrationForm()
#     if form.validate():
#         author = Author()
#         author.nickname = form.username.data
#         author.email = form.email.data
#         author.hashed_password = generate_password_hash(form.password.data)
#         session = create_session()
#         session.add(author)
#         session.commit()
#         os.mkdir(f"data/{author.id}")
#         return flask.redirect("/login")
#     else:
#         print(form.errors)
#     return flask.render_template('registration_creator.html', action=1, form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")
