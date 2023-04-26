import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post, put

from forms.user_put import UserPutForm
from salt import salt

blueprint_user = flask.Blueprint(
    'group_user',
    __name__,
    template_folder='templates'
)


@blueprint_user.route('/user')
@login_required
def get_user_list():
    if not current_user.is_admin:
        return redirect('/')
    users = get(f'http://localhost:5000/api/user').json()
    us = []
    for user in users:
        user1 = {}
        if "group" in user:
            user1['bigname'] = f'{user["fio"]}, {user["group"]["name"]}'
        else:
            user1['bigname'] = user["fio"]
        if not user['is_activated']:
            user1['bigname'] += ', не активирован'
        user1['id'] = user['id']
        us.append(user1)
    return render_template("user_list.html", users=us, title='Турниры')


@blueprint_user.route('/user/<int:user_id>/put/', methods=['GET', 'POST'])
@login_required
def put_user(user_id):
    if not current_user.is_admin:
        return redirect('/')
    form = UserPutForm()
    groups = get(f'http://localhost:5000/api/group/').json()
    form.group_id.choices = [(group['id'], group['name']) for group in groups]
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'group_id': form.group_id.data,
            'email': form.email.data,
            'password': form.password.data,
            'fio': form.fio.data,
            'is_female': form.gender.data,
            'is_activated': form.is_activated.data,
            'salt': salt
        }
        put(f'http://localhost:5000/api/user/{user_id}', json=data)
        return redirect(f'/user')
    user = get(f'http://localhost:5000/api/user/{user_id}').json()
    form.email.data = user['email']
    form.gender.data = user['is_female']
    form.fio.data = user['fio']
    form.is_activated.data = user['is_activated']
    if user['group_id'] is not None:
        form.group_id.data = user['group_id']
    form.submit.label.text = 'Изменить'
    return render_template('user_put.html', title='Изменение пользователя', form=form)
