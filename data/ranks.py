import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Rank(SqlAlchemyBase):
    __tablename__ = 'ranks'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    game_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("game_types.id"), primary_key=True)
    val = sqlalchemy.Column(sqlalchemy.Integer, default=1000)
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    game_type = orm.relationship('GameType')
    user = orm.relationship('User')