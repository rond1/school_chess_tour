import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


assoc_black = sqlalchemy.Table(
    'blacks',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('b_user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('b_game_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('games.id'))
)


assoc_white = sqlalchemy.Table(
    'whites',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('w_user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('w_game_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('games.id'))
)


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tour_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tours.id"))

    record = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    tour = orm.relationship('Tour')
    black = orm.relationship("User", secondary="blacks", backref="b_user_id")
    white = orm.relationship("User", secondary="whites", backref="w_user_id")