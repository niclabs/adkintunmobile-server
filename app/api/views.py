from flask_restful import Resource, reqparse
# from flask import jsonify
from .. import db
from . import api
from datetime import datetime


class Registration(Resource):
    def post(self):
        from app.models.sim import Sim
        from app.models.carrier import Carrier
        from app.models.device import Device

        post_parser = reqparse.RequestParser(bundle_errors=True)
        #SIM
        post_parser.add_argument('serial_number', required=True)
        post_parser.add_argument('carrier_id', required=True)
        #Device
        post_parser.add_argument('brand', required=True)
        post_parser.add_argument('board', required=True)
        post_parser.add_argument('build_id', required=True)
        post_parser.add_argument('device', required=True)
        post_parser.add_argument('hardware', required=True)
        post_parser.add_argument('manufacturer', required=True)
        post_parser.add_argument('model', required=True)
        post_parser.add_argument('release', required=True)
        post_parser.add_argument('release_type', required=True)
        post_parser.add_argument('product', required=True)
        post_parser.add_argument('sdk', required=True)

        args = post_parser.parse_args()

        device = Device(
                brand=args.brand,
                board=args.board,
                build_id=args.build_id,
                device=args.device,
                hardware=args.hardware,
                manufacturer=args.manufacturer,
                model=args.model,
                release=args.release,
                release_type=args.release_type,
                product=args.product,
                sdk=args.sdk,
                creation_date=datetime.now().date()
        )

        #TODO validate device

        carrier = Carrier.query.filter(Carrier.mnc == args.carrier_id).first()
        if carrier:
            sim = Sim(serial_number=args.serial_number, creation_date=datetime.now().date())
            carrier.sims.append(sim)
            db.session.add(sim)
            db.session.add(device)
            db.session.commit()
            return 'registration complete', 201

        else:
            return 'Carrier no existe', 400


class User(Resource):
    def get(self, user_id):
        from app.api.models.user import User
        user = User.query.filter_by(id=user_id).first()
        if user == None:
            # What status code should return?
            return 'user id ' + user_id + ' not found', 404
        return jsonify(user.dict)

    def put(self, user_id):
        return '', 204

    def delete(self, user_id):
        pass

api.add_resource(User, '/api/users/<string:user_id>')
api.add_resource(Registration, '/api/registration')
