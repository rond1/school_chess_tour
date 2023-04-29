import datetime

import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post, delete, put

from forms.category import CategoryPostForm
from salt import salt

blueprint_category = flask.Blueprint(
    'category_view',
    __name__,
    template_folder='templates'
)


@blueprint_category.route('/category/<int:category_id>')
def get_category(category_id):
    category = get(f'http://localhost:5000/api/category/{category_id}').json()
    category1 = {}
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
    category1['bigname'] = bigname
    category1['id'] = category_id
    category1['is_finished'] = category['is_finished']
    category1['tournament'] = {}
    category1['tournament']['id'] = category['tournament']['id']
    category1['tournament']['bigname'] = f'{category["tournament"]["name"]}. ' \
                             f'Контроль времени {category["tournament"]["game_time"]}+' \
                                         f'{category["tournament"]["move_time"]}. ' \
                                         f'Старт {category["tournament"]["start"]}. '
    category1['is_started'] = False
    if datetime.datetime.now() > datetime.datetime.strptime(category['tournament']["start"], '%Y-%m-%d %H:%M:%S'):
        category1['is_started'] = True
    category1['tours'] = []
    category1['show_participants'] = 0
    for tour in category['tours']:
        category1['show_participants'] += 1
        tour1 = {}
        bigname = ''
        if tour['number'] == 1:
            bigname += 'Финал. '
        else:
            bigname += f'1/{str(tour["number"])} финала. '
        bigname += f'Старт {tour["start"]}'
        tour1['bigname'] = bigname
        tour1['number'] = tour['number']
        tour1['games'] = []
        for game in tour['games']:
            game1 = {}
            game1['id'] = game['id']
            game1['white'] = {}
            game1['black'] = {}
            bigname_w = f'{game["white"]["fio"]} {game["white"]["group"]["name"]}'
            bigname_b = f'{game["black"]["fio"]} {game["black"]["group"]["name"]}'
            game1['white']['bigname'] = bigname_w
            game1['black']['bigname'] = bigname_b
            if game['result'] is None:
                game1['result'] = '     '
            elif game['result'] == -1:
                game1['result'] = '0 - 1'
            else:
                game1['result'] = '1 - 0'
            game1['white']['id'] = game["white"]["id"]
            game1['black']['id'] = game["black"]["id"]
            tour1['games'].append(game1)
        category1['tours'].append(tour1)
        category1['participants'] = []
    for participant in category['participants']:
        partic1 = {}
        partic1['bigname'] = f'{participant["fio"]} {participant["group"]["name"]}'
        category1['participants'].append(partic1)
    return render_template("category.html", category=category1, title='Турнир')


@blueprint_category.route('/category/post/<int:tournament_id>', methods=['GET', 'POST'])
@login_required
def post_category(tournament_id):
    form = CategoryPostForm()
    groups = get(f'http://localhost:5000/api/group/').json()
    form.groups.choices = [(group['id'], group['name']) for group in groups]
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'tournament_id': tournament_id,
            'name': form.name.data,
            'gender': form.gender.data,
            'groups': form.groups.data,
            'salt': salt
        }
        post(f'http://localhost:5000/api/category', json=data)
        return redirect(f'/tournament/{tournament_id}')
    form.gender.data = 0
    return render_template('category_post.html', title='Добавление категории', form=form)


@blueprint_category.route('/category/<int:category_id>/put', methods=['GET', 'POST'])
@login_required
def put_category(category_id):
    form = CategoryPostForm()
    groups = get(f'http://localhost:5000/api/group/').json()
    form.groups.choices = [(group['id'], group['name']) for group in groups]
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'name': form.name.data,
            'gender': form.gender.data,
            'groups': form.groups.data,
            'salt': salt
        }
        print(data)
        put(f'http://localhost:5000/api/category/{category_id}', json=data)
        return redirect(f'/category/{category_id}')
    category = get(f'http://localhost:5000/api/category/{category_id}').json()
    form.name.data = category['name']
    form.gender.data = category['gender']
    form.groups.data = [group['id'] for group in category['groups']]
    form.submit.label.text = 'Изменить'
    return render_template('category_post.html', title='Изменение категории', form=form)


@blueprint_category.route('/category/<int:category_id>/delete/<int:tournament_id>', methods=['POST'])
@login_required
def del_tournament(category_id, tournament_id):
    if current_user.is_admin:
        delete(f'http://localhost:5000/api/category/{category_id}', json={'salt': salt})
    return redirect(f'/tournament/{tournament_id}')
