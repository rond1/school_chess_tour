from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class CategoryPostForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[(1, 'Мальчики'), (-1, 'Девочки'), (0, 'Все')], coerce=int)
    groups = SelectMultipleField('Группы', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Создать')