from flask import Flask, render_template, redirect
import json
from data import db_session
from data.users import User
from data.classes import Class
from data.game_types import GameType
from data.tournaments import Tournament
from data.categories import Category
from data.ranks import Rank
from data.tours import Tour
from data.games import Game
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user

from forms.login import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
with open('settings.json', encoding="utf8") as file:
    settings = json.load(file)
header = f'{settings["school"]}.'
alt = settings["title"] + '. '
alt += ', '.join(f' {settings["country"]} {settings["region"]} '
                f'{settings["district"]} {settings["place"]}'.split())


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    tournaments = db_sess.query(Tournament).all()
    print(tournaments)
    ts = []
    for tournament in tournaments:
        row = []
        row.append(f'{tournament.name}. {tournament.game_type.name}. Контроль времени {tournament.game_time}+{tournament.move_time}. Старт {tournament.start.strftime("%Y-%m-%d-%H в %M.%S")}')
        for category in tournament.categories:
            string_category = ''
            if category.class_letter:
                string_category += f'{category.class_from}{category.class_letter} класс. '
            elif category.class_from:
                string_category += f'{category.class_from}-{category.class_to} классы. '
            elif category.year_from:
                string_category += f'{category.year_from}-{category.year_to} г.р. '
            if category.gender == 1:
                string_category += 'Мальчики. '
            elif category.gender == -1:
                string_category += 'Девочки. '
            if not string_category:
                string_category = 'Турнир для всех.'
            row.append(string_category)
        ts.append(row)

    return render_template("index.html", tournaments=ts, title='Турниры', alt=alt, header=header)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, alt=alt, header=header,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, alt=alt, header=header,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            midname=form.midname.data,
            birthday=form.birthday.data,
            is_female=bool(form.gender.data),
            phone=form.phone.data,
            telegram=form.telegram.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, alt=alt, header=header)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_activated and not user.is_admin:
                return render_template('login.html',
                                       message="Пользователь не активирован, обратитесь к администратору",
                                       title='Авторизация', form=form, alt=alt, header=header)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               title='Авторизация', form=form, alt=alt, header=header)
    return render_template('login.html', title='Авторизация', form=form, alt=alt, header=header)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/school_chess_tour.db")
    db_sess = db_session.create_session()
    if not db_sess.query(Class).all():
        user_class = Class()
        db_sess = db_session.create_session()
        db_sess.add(user_class)
        db_sess.commit()
        user = User()
        user.user_class_id = 1
        user.is_admin = True
        user.name = 'Админ'
        user.surname = 'Админов'
        user.birthday = datetime.date(2006, 11, 3)
        user.email = "admin@admin.ru"
        user.set_password('admin')
        db_sess.add(user)
        db_sess.commit()
        game_type = GameType()
        game_type.name = 'Шахматы. Классика'
        db_sess.add(game_type)
        db_sess.commit()
        game_type = GameType()
        game_type.name = 'Шахматы. Рапид'
        db_sess.add(game_type)
        db_sess.commit()
        game_type = GameType()
        game_type.name = 'Шахматы. Блиц'
        db_sess.add(game_type)
        db_sess.commit()
        tournament = Tournament()
        tournament.name = 'Новогодний турнир 2023-2024'
        tournament.game_type_id = 1
        tournament.game_time = 120
        tournament.move_time = 30
        tournament.start = datetime.datetime(2023, 12, 30, 15, 0, 0)
        db_sess.add(tournament)
        db_sess.commit()
        category = Category()
        category.tournament_id = 1
        category.class_from = 1
        category.class_to = 4
        category.gender = 1
        db_sess.add(category)
        db_sess.commit()
        category = Category()
        category.tournament_id = 1
        category.class_from = 9
        category.class_to = 11
        category.gender = -1
        db_sess.add(category)
        db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()
