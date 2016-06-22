from app import db
from flask_restful import Resource, reqparse
from . import api
from app import auth


class Registration(Resource):
    method_decorators = [auth.login_required]

    def post(self):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        # SIM
        post_parser.add_argument('serial_number', required=True)
        post_parser.add_argument('carrier_id', required=True)
        # Device
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
        post_parser.add_argument('device_id', required=True)

        args = post_parser.parse_args()

        return add_device_sim_carrier(args)


api.add_resource(Registration, '/api/registration')

def add_device_sim_carrier(args):
    from app.models.sim import Sim
    from app.models.carrier import Carrier
    from app.models.device import Device

    carrier = Carrier.query.filter(Carrier.mnc == args.carrier_id).first()
    if carrier:
        # TODO habrá que agregar alguna vez carriers nuevos (?)

        device = Device.store_if_no_exist(args)

        # .store_if_not_exist(args)
        sim = Sim().store_if_not_exist(args)

        # Se vinculan sim con device
        sim.devices.append(device)

        # Se vincula sim con carrier
        carrier.sims.append(sim)

        db.session.commit()
        return 'registration complete', 201

    else:
        return 'Carrier does not exist', 400
