import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post, delete, put

from forms.tour import TourPostForm
from salt import salt

blueprint_tour = flask.Blueprint(
    'tour_view',
    __name__,
    template_folder='templates'
)


@blueprint_tour.route('/tour/post/<int:category_id>', methods=['GET', 'POST'])
@login_required
def post_tour(category_id):
    form = TourPostForm()
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'category_id': category_id,
            'start': form.start.data.strftime('%Y-%m-%dT%H:%M'),
            'salt': salt
        }
        post(f'http://localhost:5000/api/tour', json=data)
        return redirect(f'/category/{category_id}')
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
    category1['tournament'] = {}
    category1['tournament']['id'] = category['tournament']['id']
    category1['tournament']['bigname'] = f'{category["tournament"]["name"]}. ' \
                                         f'Контроль времени {category["tournament"]["game_time"]}+' \
                                         f'{category["tournament"]["move_time"]}. ' \
                                         f'Старт {category["tournament"]["start"]}. '
    return render_template('tour_post.html', title='Создание тура', form=form, category=category1)


# @blueprint_category.route('/category/<int:category_id>/put', methods=['GET', 'POST'])
# @login_required
# def put_category(category_id):
#     form = CategoryPostForm()
#     groups = get(f'http://localhost:5000/api/group/').json()
#     form.groups.choices = [(group['id'], group['name']) for group in groups]
#     if form.validate_on_submit() and current_user.is_admin:
#         data = {
#             'name': form.name.data,
#             'gender': form.gender.data,
#             'groups': form.groups.data,
#             'salt': salt
#         }
#         print(data)
#         put(f'http://localhost:5000/api/category/{category_id}', json=data)
#         return redirect(f'/category/{category_id}')
#     category = get(f'http://localhost:5000/api/category/{category_id}').json()
#     form.name.data = category['name']
#     form.gender.data = category['gender']
#     form.groups.data = [group['id'] for group in category['groups']]
#     form.submit.label.text = 'Изменить'
#     return render_template('category_post.html', title='Изменение категории', form=form)


# @blueprint_category.route('/category/<int:category_id>/delete/<int:tournament_id>', methods=['POST'])
# @login_required
# def del_tournament(category_id, tournament_id):
#     if current_user.is_admin:
#         delete(f'http://localhost:5000/api/category/{category_id}', json={'salt': salt})
#     return redirect(f'/tournament/{tournament_id}')
