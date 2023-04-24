import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


association_table1 = sqlalchemy.Table(
    'cat2user',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('category_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)

association_table2 = sqlalchemy.Table(
    'cat2group',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('category_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id')),
    sqlalchemy.Column('group_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tournament_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tournaments.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    gender = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    tournament = orm.relationship('Tournament')
    tours = orm.relationship('Tour', back_populates='category')

    participants = orm.relationship("User", secondary="cat2user", backref="category_id")
    groups = orm.relationship("Group", secondary="cat2group", backref="category_id")