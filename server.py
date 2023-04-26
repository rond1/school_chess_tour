from flask import Flask, render_template, redirect
from data import db_session, tournament_resources, tournament_view, \
    category_resources, tour_resources, game_resources, group_resources, user_resources, category_view, tour_view, \
    game_view, group_view, user_view
from data.users import User
from data.tournaments import Tournament
from data.categories import Category
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user

from forms.login import LoginForm
from forms.user import RegisterForm

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return redirect('/tournament')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            fio=form.fio.data,
            email=form.email.data,
            is_female=bool(form.gender.data)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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
                                       title='Авторизация', form=form)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               title='Авторизация', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/school_chess_tour.db")
    db_sess = db_session.create_session()
    if not db_sess.query(User).all():
        user = User()
        user.is_admin = True
        user.fio = 'Админ'
        user.email = "admin@admin.ru"
        user.set_password('admin')
        db_sess.add(user)
        db_sess.commit()
        tournament = Tournament()
        tournament.name = 'Новогодний турнир 2023-2024'
        tournament.game_time = 120
        tournament.move_time = 30
        tournament.start = datetime.datetime(2023, 12, 30, 15, 0, 0)
        db_sess.add(tournament)
        db_sess.commit()
        category = Category()
        category.tournament_id = 1
        category.gender = 1
        category.name = 'мальчики до 15'
        db_sess.add(category)
        db_sess.commit()
        category = Category()
        category.tournament_id = 1
        category.name = 'девочки до 15'
        category.gender = -1
        db_sess.add(category)
        db_sess.commit()
    # для списка объектов
    api.add_resource(tournament_resources.TournamentListResource, '/api/tournament/')
    api.add_resource(category_resources.CategoryListResource, '/api/category/')
    api.add_resource(tour_resources.TourListResource, '/api/tour/')
    api.add_resource(group_resources.GroupListResource, '/api/group/')
    api.add_resource(user_resources.UserListResource, '/api/user/')

    # для одного объекта
    api.add_resource(tournament_resources.TournamentResource, '/api/tournament/<int:tournament_id>')
    api.add_resource(category_resources.CategoryResource, '/api/category/<int:category_id>')
    api.add_resource(tour_resources.TourResource, '/api/tour/<int:tour_id>')
    api.add_resource(game_resources.GameResource, '/api/game/<int:game_id>')
    api.add_resource(group_resources.GroupResource, '/api/group/<int:group_id>')
    api.add_resource(user_resources.UserResource, '/api/user/<int:user_id>')

    app.register_blueprint(tournament_view.blueprint_tournament)
    app.register_blueprint(category_view.blueprint_category)
    app.register_blueprint(tour_view.blueprint_tour)
    app.register_blueprint(game_view.blueprint_game)
    app.register_blueprint(group_view.blueprint_group)
    app.register_blueprint(user_view.blueprint_user)
    app.run()


if __name__ == '__main__':
    main()
