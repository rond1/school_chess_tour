from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.groups import Group
from salt import salt


def abort_if_groups_not_found(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404, message=f"Tournament {group_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('salt', required=True)


class GroupListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groups = session.query(Group).all()
        groups1 = []
        for group in groups:
            group1 = group.to_dict(
                only=('id', 'name'))
            groups1.append(group1)
        return jsonify(groups1)

    def post(self):
        args = parser.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        group = Group(
            name=args['name'],
        )
        if session.query(Group).filter(Group.name == args['name']).first():
            return jsonify({'error': 'Такая группа уже есть'})
        session.add(group)
        session.commit()
        return jsonify({'success': 'OK'})


parser1 = reqparse.RequestParser()
parser1.add_argument('name')
parser1.add_argument('id', type=int)
parser1.add_argument('salt', required=True)


class GroupResource(Resource):
    def get(self, group_id):
        abort_if_groups_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        group1 = {}
        group1['name'] = group.name
        users = []
        for user in group.users:
            users.append(user.to_dict(
                only=('id', 'fio', 'is_female')))
        group1['users'] = users
        return jsonify(group1)

    def put(self, group_id):
        args = parser1.parse_args()
        if args['salt'] != salt:
            return jsonify({'error': 'unsalted'})
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        if args['name']:
            group.name = args['name']
            session.commit()
            return jsonify({'success': 'OK'})
        if args['id']:
            for user in group.users:
                user.group_id = args['id']
            session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, group_id):
        abort_if_groups_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        session.delete(group)
        session.commit()
        return jsonify({'success': 'OK'})