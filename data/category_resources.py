import datetime

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.categories import Category


def abort_if_tournaments_not_found(categories_id):
    session = db_session.create_session()
    categories = session.query(Category).get(categories_id)
    if not categories:
        abort(404, message=f"News {categories_id} not found")


class TournamentResource(Resource):
    def get(self):
        pass

    def delete(self):
        pass


parser = reqparse.RequestParser()
parser.add_argument('class_letter', required=False)
parser.add_argument('tournament_id', required=True, type=int)
parser.add_argument('year_from', required=False, type=int)
parser.add_argument('year_to', required=False, type=int)
parser.add_argument('class_from', required=False, type=int)
parser.add_argument('class_to', required=False, type=int)
parser.add_argument('class_letter', required=False)
parser.add_argument('gender', required=True, type=int)
parser.add_argument('system', required=True, type=int)
parser.add_argument('salt', required=True)


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create__session()
        tournaments1 = []
        if filter == 'arch':
            tournaments = session.query(Tournament).filter(Tournament.is_finished == True)
        elif filter == 'active':
            tournaments = session.query(Tournament).filter(Tournament.is_finished == False)
        else:
        tournaments = session.query(Tournament).all()
        for tournament in tournaments:
            tournament1 = {}
            tournament1['id'] = tournament.id
            tournament1['name'] = tournament.name
            tournament1['game_type'] = tournament.game_type.name
            tournament1['game_time'] = tournament.game_time
            tournament1['move_time'] = tournament.move_time
            tournament1['start'] = tournament.start.strftime("%Y-%m-%d %H:%M")
            tournament1['categories'] = []
            tournament1['is_finished'] = tournament.is_finished
            for category in tournament.categories:
                tournament1['categories'].append(category.to_dict(only=('id', 'class_from', 'class_to', 'class_letter', 'year_from', 'year_to', 'gender', 'system')))
            tournaments1.append(tournament1)

        return jsonify(tournaments1)

    def post(self, filter):
        args = parser.parse_args()
        if args['salt'] != 'mcadfmpfojhnmryktm[wrtnb[wrinb[wirtbn[2i91tnmb1r5k1nfb5615wkinbwt':
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        tournaments = Tournament(
            name=args['name'],
            game_time=args['game_time'],
            move_time=args['move_time'],
            start=datetime.datetime.strptime(args['start'], '%Y-%m-%dT%H:%M'),
            game_type_id=args['game_type_id']
        )
        session.add(tournaments)
        session.commit()
        return jsonify({'success': 'OK'})