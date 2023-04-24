import datetime
import math

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.tours import Tour
from data.categories import Category
from data.games import Game
from salt import salt


def abort_if_tour_not_found(tour_id):
    session = db_session.create_session()
    tour = session.query(Tour).get(tour_id)
    if not tour:
        abort(404, message=f"Tournament {tour_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('category_id', required=True, type=int)
parser.add_argument('start', required=True)
parser.add_argument('salt', required=True)


class TourListResource(Resource):
    def post(self):
        args = parser.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        category = session.query(Category).get(args['category_id'])
        if len(category.participants) < 2:
            return jsonify({'error': 'МАЛО УЧАСТНИКОВ ДЛЯ ПЕРВОГО ТУРА'})
        if category.is_finished:
            return jsonify({'error': 'ВСЕ ИГРЫ В КАТЕГОРИИ ЗАКОНЧЕНЫ'})
        tour = Tour(
            category_id=args['category_id'],
            start=datetime.datetime.strptime(args['start'], '%Y-%m-%dT%H:%M')
        )
        session.add(tour)
        session.commit()
        if len(tour.category.tours) == 1:
            tour.number = int(2 ** (math.log2(len(tour.category.participants) - 1) // 1))
            for i in range(len(tour.category.participants) - tour.number):
                game = Game()
                game.tour = tour
                game.white.append(tour.category.participants[i * 2])
                game.black.append(tour.category.participants[i * 2 + 1])
                session.add(game)
                session.commit()
        else:
            ids = [i for i in range(len(tour.category.participants))]
            for t in tour.category.tours:
                for g in t.games:
                    if g.result is not None:
                        if g.result == -1:
                            ids.remove(tour.category.participants.index(g.white[0]))
                        else:
                            ids.remove(tour.category.participants.index(g.black[0]))
            tour.number = len(ids) // 2
            if len(tour.category.tours) % 2 == 0:
                ids.reverse()
            for i in range(tour.number):
                game = Game()
                game.tour = tour
                game.white.append(tour.category.participants[ids[i * 2]])
                game.black.append(tour.category.participants[ids[i * 2 + 1]])
                session.add(game)
                session.commit()
        session.commit()
        return jsonify({'success': 'OK'})


parser2 = reqparse.RequestParser()
parser2.add_argument('salt', required=True)

parser1 = reqparse.RequestParser()
parser1.add_argument('number', required=True, type=int)
parser1.add_argument('start', required=True)


class TourResource(Resource):
    def put(self, tour_id):
        args = parser2.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        tour = session.query(Tour).get(tour_id)
        args = parser1.parse_args()
        tour.number = args['number']
        tour.start = datetime.datetime.strptime(args['start'], '%Y-%m-%dT%H:%M')
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, tour_id):
        abort_if_tour_not_found(tour_id)
        session = db_session.create_session()
        tour = session.query(Tour).get(tour_id)
        session.delete(tour)
        session.commit()
        return jsonify({'success': 'OK'})