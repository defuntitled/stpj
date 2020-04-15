import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Customchannel(SqlAlchemyBase):
    __tablename__ = 'customchannels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"))
    owner = orm.relationship("User", back_populates="customchannels")
    author = orm.relationship("Authorcannel", back_populates="customchannels")

