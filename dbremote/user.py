import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash

follow_table = sqlalchemy.Table('followers', SqlAlchemyBase.metadata,
                                sqlalchemy.Column('follower_id', sqlalchemy.Integer,
                                                  sqlalchemy.ForeignKey('users.id')),
                                sqlalchemy.Column('followed_id', sqlalchemy.Integer,
                                                  sqlalchemy.ForeignKey('users.id'))
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
    followed = orm.relationship(
        'User', secondary=follow_table,
        primaryjoin=(follow_table.c.follower_id == id),
        secondaryjoin=(follow_table.c.followed_id == id),
        backref=orm.backref('follow_table', lazy='dynamic'), lazy='dynamic')
    utype = sqlalchemy.Column(sqlalchemy.Boolean,
                              default=False)
    stories = orm.relationship("Story", back_populates='author')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

