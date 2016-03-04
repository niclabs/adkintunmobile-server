from flask_restful import Resource
# from flask import jsonify
from .. import db
from . import api
from datetime import datetime

class Registration(Resource):
    def post(self):
        from app.models.sim import Sim
        sim = Sim(creation_date=datetime.now().date())
        db.session.add(sim)
        db.session.commit()
        return 'registration complete', 201

# class User(Resource):
#     def get(self, user_id):
#         from app.api.models.user import User
#         user = User.query.filter_by(id=user_id).first()
#         if user == None:
#             # What status code should return?
#             return 'user id ' + user_id + ' not found', 404
#         return jsonify(user.dict)
#
#     def put(self, user_id):
#         return '', 204
#
#     def delete(self, user_id):
#         pass

#api.add_resource(User, '/api/users/<string:user_id>')
api.add_resource(Registration, '/api/registration')
