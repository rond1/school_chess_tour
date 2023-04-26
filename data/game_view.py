import flask
from flask import render_template, redirect
from flask_login import login_required, current_user
from requests import get, post, delete, put

from forms.game import GamePutForm
from salt import salt

blueprint_game = flask.Blueprint(
    'game_view',
    __name__,
    template_folder='templates'
)


@blueprint_game.route('/game/<int:game_id>/put/<int:category_id>', methods=['GET', 'POST'])
@login_required
def put_game(game_id, category_id):
    form = GamePutForm()
    if form.validate_on_submit() and current_user.is_admin:
        data = {
            'result': form.result.data,
            'salt': salt
        }
        put(f'http://localhost:5000/api/game/{game_id}', json=data)
        return redirect(f'/category/{category_id}')
    return render_template('game_put.html', title='Установка результата', form=form)
