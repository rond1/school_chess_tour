import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'tour2user',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('tournament_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tournaments.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class Tournament(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tournaments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    game_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    move_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

    start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    categories = orm.relationship('Category', back_populates='tournament')

    demands = orm.relationship("User", secondary="tour2user", backref="tournament_id")
