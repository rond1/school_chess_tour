import datetime

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.tournaments import Tournament


def abort_if_tournaments_not_found(tournaments_id):
    session = db_session.create_session()
    tournaments = session.query(Tournament).get(tournaments_id)
    if not tournaments:
        abort(404, message=f"News {tournaments_id} not found")


class TournamentResource(Resource):
    def get(self, tournament_id):
        abort_if_tournaments_not_found(tournament_id)
        session = db_session.create_session()
        tournaments = session.query(Tournament).get(tournament_id)
        return jsonify({'news': tournaments.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, tournament_id):
        abort_if_tournaments_not_found(tournament_id)
        session = db_session.create_session()
        tournaments = session.query(Tournament).get(tournament_id)
        session.delete(tournaments)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('game_type_id', required=True, type=int)
parser.add_argument('start', required=True)
parser.add_argument('game_time', required=True, type=int)
parser.add_argument('move_time', required=True, type=int)
parser.add_argument('salt', required=True)


class TournamentListResource(Resource):
    def get(self, filter):
        session = db_session.create_session()
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