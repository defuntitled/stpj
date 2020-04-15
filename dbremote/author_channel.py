import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Authorchannel(SqlAlchemyBase):
    __tablename__ = 'authorchannels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    author = orm.relationship("User", back_populates="authorchannels")
    follower_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("customchannels.id"))
    follower = orm.relationship("Customchannel", back_populates="authorchannels")

