from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.categories import Category
from data.groups import Group
from data.users import User
from salt import salt


def abort_if_categories_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Tournament {category_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('gender', required=True, type=int)
parser.add_argument('tournament_id', required=True, type=int)
parser.add_argument('groups', required=False, type=int, action='append')
parser.add_argument('salt', required=True)


class CategoryListResource(Resource):
    def post(self):
        args = parser.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        category = Category(
            name=args['name'],
            gender=args['gender'],
            tournament_id=args['tournament_id']
        )
        session.add(category)
        for group_id in args['groups']:
            group = session.query(Group).get(group_id)
            category.groups.append(group)
        session.commit()
        return jsonify({'success': 'OK'})


parser1 = reqparse.RequestParser()
parser1.add_argument('user_id', required=False, type=int)
parser1.add_argument('name', required=False)
parser1.add_argument('gender', required=False, type=int)
parser1.add_argument('groups', required=False, type=int, action='append')
parser1.add_argument('salt', required=True)


class CategoryResource(Resource):
    def get(self, category_id):
        abort_if_categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        category1 = category.to_dict(
            only=('name', 'gender', 'is_finished'))
        category1['tournament'] = category.tournament.to_dict(
            only=('id', 'name', 'game_time', 'move_time', 'start', 'is_finished'))
        participants = []
        for participant in category.participants:
            participant1 = participant.to_dict(
                only=('id', 'fio', 'is_female'))
            participant1['group'] = participant.group.to_dict(only=('id', 'name'))
            participants.append(participant1)
        category1['participants'] = participants
        tours = []
        for tour in category.tours:
            tour1 = tour.to_dict(
                only=('id', 'number', 'category_id', 'start', 'is_finished'))
            games = []
            for game in tour.games:
                game1 = {}
                game1['id'] = game.id
                game1['result'] = game.result
                game1['white'] = game.white[0].to_dict(only=('id', 'fio', 'is_female'))
                game1['black'] = game.black[0].to_dict(only=('id', 'fio', 'is_female'))
                for partic in category1['participants']:
                    if partic['id'] == game1['white']['id']:
                        game1['white']['group'] = partic['group']
                    elif partic['id'] == game1['black']['id']:
                        game1['black']['group'] = partic['group']
                games.append(game1)
            tour1['games'] = games
            tours.append(tour1)
        category1['tours'] = tours
        groups = []
        for group in category.groups:
            group1 = group.to_dict(
                only=('id', 'name'))
            groups.append(group1)
        category1['groups'] = groups
        return jsonify(category1)

    def put(self, category_id):
        args = parser1.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        if args['user_id'] is not None:
            if args['user_id'] == 0:
                for demand in category.tournament.demands:
                    if (demand.group_id in [group.id for group in category.groups]) \
                            and (category.gender == 0 or (category.gender == -1 and demand.is_female)
                                 or (category.gender == 1 and not demand.is_female)):
                        category.participants.append(demand)
                        session.commit()
                return jsonify({'success': 'OK'})
            user = session.query(User).get(args['user_id'])
            category.participants.append(user)
            session.commit()
            return jsonify({'success': 'OK'})
        if args['name'] is not None:
            category.name = args['name']
        if args['gender'] is not None:
            category.gender = args['gender']
        if args['groups'] is not None:
            for group in category.groups:
                category.groups.remove(group)
            for group_id in args['groups']:
                group = session.query(Group).get(group_id)
                category.groups.append(group)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, category_id):
        abort_if_categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        for tour in category.tours:
            for game in tour.games:
                session.delete(game)
        for tour in category.tours:
            session.delete(tour)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})