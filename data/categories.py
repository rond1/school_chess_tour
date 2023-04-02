import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tournament_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tournaments.id"))

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    year_from = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year_to = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    class_from = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    class_to = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    class_letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    system = sqlalchemy.Column(sqlalchemy.Integer, default=2)

    tournament = orm.relationship('Tournament')
    tours = orm.relationship('Tour', back_populates='category')