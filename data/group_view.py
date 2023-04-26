import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post, put

from forms.group import GroupPostForm
from salt import salt

blueprint_group = flask.Blueprint(
    'group_view',
    __name__,
    template_folder='templates'
)


@blueprint_group.route('/group')
@login_required
def get_group_list():
    if not current_user.is_admin:
        return redirect('/')
    groups = get(f'http://localhost:5000/api/group').json()
    gs = []
    for group in groups:
        gs.append({'id': group['id'], 'name': group['name']})
    return render_template("group_list.html", groups=gs, title='Турниры')


@blueprint_group.route('/group/post/', methods=['GET', 'POST'])
@login_required
def post_group():
    if not current_user.is_admin:
        return redirect('/')
    form = GroupPostForm()
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'name': form.name.data,
            'salt': salt
        }
        post(f'http://localhost:5000/api/group', json=data)
        return redirect('/group')
    return render_template('group_post.html', title='Добавление группы', form=form)


@blueprint_group.route('/group/<int:group_id>/put/', methods=['GET', 'POST'])
@login_required
def put_group(group_id):
    if not current_user.is_admin:
        return redirect('/')
    form = GroupPostForm()
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'name': form.name.data,
            'salt': salt
        }
        put(f'http://localhost:5000/api/group/{group_id}', json=data)
        return redirect(f'/group')
    group = get(f'http://localhost:5000/api/group/{group_id}').json()
    form.name.data = group['name']
    form.submit.label.text = 'Изменить'
    return render_template('group_post.html', title='Изменение группы', form=form)
