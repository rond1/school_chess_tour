from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email


class UserPutForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Новый пароль')
    fio = StringField('ФИО', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[(0, 'М'), (1, 'Ж')], validators=[DataRequired()])
    group_id = SelectField('Группа', validators=[DataRequired()], coerce=int)
    is_activated = BooleanField('Активировать пользователя')
    submit = SubmitField('Изменить')