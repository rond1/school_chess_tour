import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class GameType(SqlAlchemyBase):
    __tablename__ = 'game_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    win = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    loss = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    draw = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0.5)

    tournaments = orm.relationship('Tournament', back_populates='game_type')
    ranks = orm.relationship('Rank', back_populates='game_type')