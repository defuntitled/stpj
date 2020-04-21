import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

comment_table = sqlalchemy.Table('comments_follow', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('story_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('stories.id')),
                                 sqlalchemy.Column('comment_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('comments.id'),))


class Story(SqlAlchemyBase):
    __tablename__ = 'stories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("authors.id"))
    user = orm.relation('Author')

    cover = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    head = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    commented = orm.relation("Comment", secondary=comment_table)


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    head = sqlalchemy.Column(sqlalchemy.String, nullable=True)
