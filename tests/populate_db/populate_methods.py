from sqlalchemy.exc import IntegrityError

from app import db
from app.data.populate_methods import populate_carriers


def populate_standard_test():
    from app.models.antenna import Antenna
    from app.models.carrier import Carrier
    populate_carriers()
    antenna1 = Antenna(cid=1259355, lac=55700, lat=0.2, lon=0.1)
    antenna2 = Antenna(cid=1277982, lac=55700, lat=0.3, lon=0.4)
    carrier = Carrier.query.filter(Carrier.mnc == 2 and Carrier.mcc == 730).first()
    carrier.antennas.append(antenna1)
    carrier.antennas.append(antenna2)
    db.session.add(antenna1)
    db.session.add(antenna2)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
