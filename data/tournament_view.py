import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post

from data import db_session
from forms.tournament_add import TournamentAddForm
from main import alt, header

blueprint = flask.Blueprint(
    'tournament_view',
    __name__,
    template_folder='templates'
)

CAT_SYS = ['Олимпийская', 'Круговик', 'Швейцарская (Бухгольц, Бухгольц усеченный, Кол-во побед)',
           'Швейцарская (Бухгольц, Кол-во побед, Бухгольц усеченный)',
           'Швейцарская (Кол-во побед, Бухгольц, Бухгольц усеченный)',
           'Швейцарская (Кол-во побед, Бухгольц усеченный, Бухгольц)',
           'Швейцарская (Бухгольц усеченный, Кол-во побед, Бухгольц)',
           'Швейцарская (Бухгольц усеченный, Бухгольц, Кол-во побед)']


@blueprint.route('/tournament/') # tournament/<int:id>
def get_tournament_redirect():
    return redirect('/tournament/all')


@blueprint.route('/tournament/add/', methods=['GET', 'POST']) # tournament/<int:id>
@login_required
def add_tournament():
    form = TournamentAddForm()
    game_types = get('http://localhost:5000/api/gametype/').json()
    choices = []
    for game_type in game_types:
        choices.append((game_type['id'], game_type['name']))
    form.game_type_id.choices = choices
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'name': form.name.data,
            'game_time': form.game_time.data,
            'move_time': form.move_time.data,
            'start': form.start.data.strftime('%Y-%m-%dT%H:%M'),
            'game_type_id': form.game_type_id.data,
            'salt': 'mcadfmpfojhnmryktm[wrtnb[wrinb[wirtbn[2i91tnmb1r5k1nfb5615wkinbwt'
        }
        post(f'http://localhost:5000/api/tournament/add', json=data)
        return redirect('/tournament/all')
    return render_template('tournament_add.html', title='Добавление турнира',
                           form=form, alt=alt, header=header)


@blueprint.route('/tournament/<filter>') # tournament/<int:id>
def get_tournament(filter):
    tournaments = get(f'http://localhost:5000/api/tournament/{filter}').json()
    ts = []
    ids = []
    for tournament in tournaments:
        row = [f'{tournament["name"]}. {tournament["game_type"]}. '
            f'Контроль времени {tournament["game_time"]}+{tournament["move_time"]}. Старт {tournament["start"]}. ']
        if tournament['is_finished']:
            row += 'Завершен'
        row_id = [tournament["id"]]
        for category in tournament["categories"]:
            string_category = ''
            if category["class_letter"]:
                string_category += f'{category["class_from"]}{category["class_letter"]} класс. '
            elif category["class_from"]:
                string_category += f'{category["class_from"]}-{category["class_to"]} классы. '
            elif category["year_from"]:
                string_category += f'{category["year_from"]}-{category["year_to"]} г.р. '
            if category["gender"] == 1:
                string_category += 'Мальчики. '
            elif category["gender"] == -1:
                string_category += 'Девочки. '
            if not string_category:
                string_category = 'Турнир для всех.'
            string_category += CAT_SYS[category['system']]
            row.append(string_category)
            row_id.append(category['id'])
        ts.append(row)
        ids.append(row_id)

    return render_template("tournament_list.html", tournaments=ts, ids=ids, title='Турниры', alt=alt, header=header)