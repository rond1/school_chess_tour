from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GroupPostForm(FlaskForm):
    name = StringField('Название группы', validators=[DataRequired()])
    submit = SubmitField('Добавить')