import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))

    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    is_female = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    is_activated = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    midname = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    birthday = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    reg_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    telegram = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)

    user_class = orm.relationship('Class')
    ranks = orm.relationship('Rank', back_populates='user')
    blacks = orm.relationship("Game", secondary="blacks", backref="black")
    whites = orm.relationship("Game", secondary="whites", backref="white")

    def __repr__(self):
        return f"<User> {self.id} {self.login} {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)