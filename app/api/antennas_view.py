from app import application, auth
from app.models.antenna import Antenna
from app.public.views import page_not_found
from flask import jsonify


@application.route("/antenna/<id>", methods=["GET"])
@auth.login_required
def get_antenna_info(id):
    antenna = Antenna.query.filter(Antenna.id == id).first()
    if antenna:
        return jsonify(antenna.serialize)
    else:
        return page_not_found()
