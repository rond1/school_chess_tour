import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class GameType(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    win = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=1.0)
    loss = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.0)
    draw = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.5)

    tournaments = orm.relationship('Tournament', back_populates='game_type')
    ranks = orm.relationship('Rank', back_populates='game_type')