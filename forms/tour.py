from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired


class TourPostForm(FlaskForm):
    start = DateTimeLocalField('Начало', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Создать')