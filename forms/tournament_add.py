from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired


class TournamentAddForm(FlaskForm):
    name = StringField('Название турнира', validators=[DataRequired()])

    game_time = IntegerField('Время общее (мин)', validators=[DataRequired()])
    move_time = IntegerField('Кол-во секунд на каждый ход', validators=[DataRequired()])

    start = DateTimeLocalField('Начало', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    game_type_id = SelectField('Тип игры', validators=[DataRequired()])

    submit = SubmitField('Создать')