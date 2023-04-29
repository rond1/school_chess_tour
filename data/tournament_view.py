import datetime

import flask
from flask import render_template, redirect, request
from flask_login import login_required, current_user
from requests import get, post, delete, put

from forms.tournament import TournamentPostForm
from salt import salt

blueprint_tournament = flask.Blueprint(
    'tournament_view',
    __name__,
    template_folder='templates'
)


@blueprint_tournament.route('/tournament/')
def get_tournament_list():
    tournaments = get(f'http://localhost:5000/api/tournament').json()
    ts = []
    ids = []
    for tournament in tournaments:
        row = [f'{tournament["name"]}. '
            f'Контроль времени {tournament["game_time"]}+{tournament["move_time"]}. Старт {tournament["start"]}. ']
        if tournament['is_finished']:
            row[0] += 'Завершен'
        elif datetime.datetime.now() < datetime.datetime.strptime(tournament["start"], '%Y-%m-%d %H:%M:%S'):
            row[0] += 'Приём заявок'
        else:
            row[0] += 'Турнир идёт'
        ts.append(row)
        ids.append(tournament["id"])

    return render_template("tournament_list.html", tournaments=ts, ids=ids, title='Турниры')


@blueprint_tournament.route('/tournament/<int:tournament_id>') # tournament/<int:id>
def get_tournament(tournament_id):
    tournament = get(f'http://localhost:5000/api/tournament/{tournament_id}').json()
    tournament1 = {}
    tournament1['bigname'] = f'{tournament["name"]}. ' \
                             f'Контроль времени {tournament["game_time"]}+{tournament["move_time"]}. Старт {tournament["start"]}. '
    tournament1['is_started'] = True
    if tournament['is_finished']:
        tournament1['bigname'] += 'Завершен'
    elif datetime.datetime.now() < datetime.datetime.strptime(tournament["start"], '%Y-%m-%d %H:%M:%S'):
        tournament1['bigname'] += 'Приём заявок'
        tournament1['is_started'] = False
    else:
        tournament1['bigname'] += 'Турнир идёт'
    tournament1['id'] = tournament_id
    tournament1['categories'] = []
    tournament1['demands'] = []
    for category in tournament["categories"]:
        bigname = category['name'] + '. '
        if category["gender"] == 1:
            bigname += 'Мальчики. '
        elif category["gender"] == -1:
            bigname += 'Девочки. '
        else:
            bigname += 'Турнир для всех.'
        bigname += ' Группы: '
        names = []
        for group in category['groups']:
            names.append(group['name'])
        bigname += ', '.join(names)
        tournament1['categories'].append({'id': category['id'], 'bigname': bigname})
    tournament1['current_user'] = 0
    if current_user.is_authenticated:
        tournament1['current_user'] = current_user.id
    for demand in tournament['demands']:
        bigname = f'{demand["fio"]} {demand["group"]["name"]}'
        tournament1['demands'].append({'id': demand['id'], 'bigname': bigname})
        if current_user.is_authenticated:
            if demand['id'] == current_user.id:
                tournament1['current_user'] = 0
    return render_template("tournament.html", tournament=tournament1, title='Турнир')


@blueprint_tournament.route('/tournament/post/', methods=['GET', 'POST'])
@login_required
def post_tournament():
    form = TournamentPostForm()
    if form.validate_on_submit() and current_user.is_admin and form.start.data > datetime.datetime.now():
        data = {
            'name': form.name.data,
            'game_time': form.game_time.data,
            'move_time': form.move_time.data,
            'start': form.start.data.strftime('%Y-%m-%dT%H:%M'),
            'salt': salt
        }
        post(f'http://localhost:5000/api/tournament', json=data)
        return redirect('/tournament')
    return render_template('tournament_post.html', title='Добавление турнира', form=form)


@blueprint_tournament.route('/tournament/<int:tournament_id>/put/', methods=['GET', 'POST'])
@login_required
def put_tournament(tournament_id):
    form = TournamentPostForm()
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'name': form.name.data,
            'game_time': form.game_time.data,
            'move_time': form.move_time.data,
            'start': form.start.data.strftime('%Y-%m-%dT%H:%M'),
            'salt': salt
        }
        put(f'http://localhost:5000/api/tournament/{tournament_id}', json=data)
        return redirect(f'/tournament/{tournament_id}')
    tournament = get(f'http://localhost:5000/api/tournament/{tournament_id}').json()
    form.name.data = tournament['name']
    form.game_time.data = tournament['game_time']
    form.move_time.data = tournament['move_time']
    form.start.data = datetime.datetime.strptime(tournament['start'], '%Y-%m-%d %H:%M:%S')
    form.submit.label.text = 'Изменить'
    return render_template('tournament_post.html', title='Изменение турнира', form=form)


@blueprint_tournament.route('/tournament/<int:tournament_id>/demand/', methods=['POST'])
@login_required
def demand_tournament(tournament_id):
    if current_user.is_activated and not current_user.is_admin:
        put(f'http://localhost:5000/api/tournament/{tournament_id}', json={'user_id': current_user.id, 'salt': salt})
    return redirect(f'/tournament/{tournament_id}')


@blueprint_tournament.route('/tournament/<int:tournament_id>/participants/', methods=['POST'])
@login_required
def participants_tournament(tournament_id):
    if current_user.is_admin:
        tournament = get(f'http://localhost:5000/api/tournament/{tournament_id}').json()
        for category in tournament['categories']:
            put(f'http://localhost:5000/api/category/{category["id"]}', json={'user_id': 0, 'salt': salt})
    return redirect(f'/tournament/{tournament_id}')


@blueprint_tournament.route('/tournament/<int:tournament_id>/delete/', methods=['POST'])
@login_required
def del_tournament(tournament_id):
    if current_user.is_admin:
        user_id = int(request.form.get('user_id'))
        delete(f'http://localhost:5000/api/tournament/{tournament_id}', json={'salt': salt, 'user_id': user_id})
    return redirect('/tournament')
