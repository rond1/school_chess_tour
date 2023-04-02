from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    midname = StringField('Отчество')
    birthday = DateField('Дата рождения', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[(0, 'М'), (1, 'Ж')], validators=[DataRequired()])
    phone = StringField('Номер телефона')
    telegram = StringField('Имя')
    submit = SubmitField('Зарегистрироваться')