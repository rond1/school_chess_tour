from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.game_types import GameType


def abort_if_game_type_not_found(game_type_id):
    session = db_session.create_session()
    game_type = session.query(GameType).get(game_type_id)
    if not game_type:
        abort(404, message=f"Game type {game_type_id} not found")


class GameTypeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        game_types = session.query(GameType).all()
        return jsonify([game_type.to_dict(only=('id', 'name', 'win', 'loss', 'draw')) for game_type in game_types])