import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Tour(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tours'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    coeff = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    category = orm.relationship('Category')
    games = orm.relationship('Game', back_populates='tour')