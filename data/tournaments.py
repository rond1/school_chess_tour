import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Tournament(SqlAlchemyBase):
    __tablename__ = 'tournaments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    game_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("game_types.id"))

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    game_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    move_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

    start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    categories = orm.relationship('Category', back_populates='tournament')
    game_type = orm.relationship('GameType')