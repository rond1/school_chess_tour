from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    fio = StringField('ФИО', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[(0, 'М'), (1, 'Ж')], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')