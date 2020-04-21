import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase

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
    author = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    followed = orm.relation("Author", secondary=follow_table)


class Author(SqlAlchemyBase, UserMixin):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=False)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    stories = orm.relation("Story", back_populates='authors')
