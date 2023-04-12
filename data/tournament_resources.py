import datetime

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.tournaments import Tournament


def abort_if_tournaments_not_found(tournament_id):
    session = db_session.create_session()
    tournament = session.query(Tournament).get(tournament_id)
    if not tournament:
        abort(404, message=f"Tournament {tournament_id} not found")


class TournamentResource(Resource):
    def get(self, tournament_id):
        abort_if_tournaments_not_found(tournament_id)
        session = db_session.create_session()
        tournament = session.query(Tournament).get(tournament_id)
        tournament = tournament.to_dict(
            only=('name', 'game_time', 'move_time', 'start', 'is_finished'))
        tournament['start'] = tournament['start'].strftime("%Y-%m-%d %H:%M")
        return jsonify(tournament)

    def delete(self, tournament_id):
        abort_if_tournaments_not_found(tournament_id)
        session = db_session.create_session()
        tournament = session.query(Tournament).get(tournament_id)
        session.delete(tournament)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('start', required=True)
parser.add_argument('game_time', required=True, type=int)
parser.add_argument('move_time', required=True, type=int)
parser.add_argument('is_finished', required=True, type=int)
parser.add_argument('salt', required=True)


class TournamentListResource(Resource):
    def get(self, filter):
        session = db_session.create_session()
        tournaments = session.query(Tournament).all()
        for tournament in tournaments:
            tournament1 = {}
            tournament1['id'] = tournament.id
            tournament1['name'] = tournament.name
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
            start=datetime.datetime.strptime(args['start'], '%Y-%m-%dT%H:%M')
        )
        session.add(tournaments)
        session.commit()
        return jsonify({'success': 'OK'})