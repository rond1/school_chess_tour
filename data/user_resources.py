from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.games import Game
from data.users import User
from salt import salt


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Tournament {user_id} not found")


parser1 = reqparse.RequestParser()
parser1.add_argument('fio', required=True)
parser1.add_argument('email', required=True)
parser1.add_argument('is_female', required=True, type=bool)
parser1.add_argument('password', required=True)
parser1.add_argument('salt', required=True)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).order_by(User.is_activated).all()
        users1 = []
        for user in users:
            user1 = user.to_dict(only=('id', 'fio', 'is_female', 'email', 'is_activated'))
            if user.group is not None:
                user1['group'] = user.group.to_dict(only=('id', 'name'))
            users1.append(user1)
        return jsonify(users1)

    def post(self):
        args = parser1.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        user = User(
            fio=args['fio'],
            email=args['email'],
            is_female=args['is_female'],

        )
        user.set_password(args['password'])
        if session.query(User).filter(User.email == args['email']).first():
            return jsonify({'error': 'Такой пользователь уже есть'})
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('fio')
parser.add_argument('is_female', type=bool)
parser.add_argument('is_activated', type=bool)
parser.add_argument('password')
parser.add_argument('group_id', type=int)
parser.add_argument('salt', required=True)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user1 = user.to_dict(
            only=('id', 'fio', 'is_female', 'email', 'group_id', 'is_activated'))
        if user.group is not None:
            user1['group'] = user.group.to_dict(only=('id', 'name'))
        w_games = session.query(Game).filter(Game.white.contains(user)).all()
        games_w = []
        for w_game in w_games:
            game_w = {}
            game_w['result'] = w_game.result
            game_w['tour'] = w_game.tour.to_dict(
                only=('start', 'number'))
            game_w['tour']['category'] = {}
            game_w['tour']['category']['name'] = w_game.tour.category.name
            game_w['tour']['category']['tournament'] = w_game.tour.category.tournament.to_dict(
                only=('name', 'game_time', 'move_time'))
            games_w.append(game_w)
        user1['w_games'] = games_w
        b_games = session.query(Game).filter(Game.black.contains(user)).all()
        games_b = []
        for b_game in b_games:
            game_b = {}
            game_b['result'] = b_game.result
            game_b['tour'] = b_game.tour.to_dict(
                only=('start', 'number'))
            game_b['tour']['category'] = {}
            game_b['tour']['category']['name'] = b_game.tour.category.name
            game_b['tour']['category']['tournament'] = b_game.tour.category.tournament.to_dict(
                only=('name', 'game_time', 'move_time'))
            games_b.append(game_b)
        user1['b_games'] = games_b
        return jsonify(user1)

    def put(self, user_id):
        args = parser.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.fio = args['fio']
        user.is_female = args['is_female']
        user.is_activated = args['is_activated']
        user.group_id = args['group_id']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})