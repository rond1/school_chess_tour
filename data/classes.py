import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User', back_populates='user_class')