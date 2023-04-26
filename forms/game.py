from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class GamePutForm(FlaskForm):
    result = SelectField('Результат', choices=[(1, '1 - 0'), (-1, '0 - 1')], validators=[DataRequired()])
    submit = SubmitField('Записать')