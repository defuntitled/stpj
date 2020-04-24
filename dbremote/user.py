import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash

follow_table = sqlalchemy.Table('followers', SqlAlchemyBase.metadata,
                                sqlalchemy.Column('user_id', sqlalchemy.Integer,
                                                  sqlalchemy.ForeignKey('users.id')),
                                sqlalchemy.Column('author_id', sqlalchemy.Integer,
                                                  sqlalchemy.ForeignKey('authors.id'))
                                )


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    followed = orm.relationship("Author", secondary=follow_table)
    utype = sqlalchemy.Column(sqlalchemy.Boolean,
                              default=False)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Author(SqlAlchemyBase, UserMixin):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    stories = orm.relationship("Story", back_populates='author')
    utype = sqlalchemy.Column(sqlalchemy.Boolean,
                              default=True)
<<<<<<< HEAD
=======
    followers = orm.relationship("User", secondary=follow_table, back_populates="followed")
>>>>>>> origin/master

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
