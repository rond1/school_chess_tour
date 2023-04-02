import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


assoc_white = sqlalchemy.Table(
    'whites',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('game_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('games.id'))
)


assoc_black = sqlalchemy.Table(
    'blacks',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('game_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('games.id'))
)


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tour_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tours.id"))

    record = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    tour = orm.relationship('Tour')
    # black = orm.relationship("User", secondary="blacks", backref="user_id")
    # white = orm.relationship("User", secondary="whites", backref="user_id")