import datetime

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.games import Game
from salt import salt


def abort_if_games_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Game).get(game_id)
    if not game:
        abort(404, message=f"Tournament {game_id} not found")


parser2 = reqparse.RequestParser()
parser2.add_argument('salt', required=True)

parser1 = reqparse.RequestParser()
parser1.add_argument('record', required=False)
parser1.add_argument('result', required=True, type=int)


class GameResource(Resource):
    def get(self, game_id):
        abort_if_games_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        game1 = game.to_dict(
            only=('result', 'record'))
        game1['white'] = game.white[0].to_dict(
            only=('id', 'fio', 'is_female'))
        if game.white[0].group is not None:
            game1['white']['group'] = game.white[0].group.to_dict(only=('id', 'name'))
        game1['black'] = game.black[0].to_dict(
            only=('id', 'fio', 'is_female'))
        if game.black[0].group is not None:
            game1['black']['group'] = game.black[0].group.to_dict(only=('id', 'name'))
        return jsonify(game1)

    def put(self, game_id):
        args = parser2.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        args = parser1.parse_args()
        if args['record'] is not None:
            game.record = args['record']
        game.result = args['result']
        flag = True
        for one_game in game.tour.games:
            if not one_game.result:
                flag = False
        if flag:
            game.tour.is_finished = True
            for tour in game.tour.category.tours:
                if not tour.is_finished:
                    flag = False
                if flag and game.tour.number == 1:
                    game.tour.category.is_finished = True
                    for category in game.tour.category.tournament.categories:
                        if not category.is_finished:
                            flag = False
                        if flag:
                            game.tour.category.tournament.is_finished = True
        session.commit()
        return jsonify({'success': 'OK'})