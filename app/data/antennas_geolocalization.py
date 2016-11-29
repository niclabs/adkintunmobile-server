import requests

from app import db, application

BASE_URL = "http://opencellid.org/cell/get"

# Maintains the last antenna id searched in opencellid
LAST_ID = 0


def get_antenna_geolocalization(mcc: int, mnc: int, lac: int, cid: int, key_id: str) -> tuple:
    """
    Get the geolocalization for an antenna from OpenCellId if exist
    :param mnc: Antenna mnc
    :param mcc: Antenna mcc
    :param lac: Antena local area code
    :param cid: Antenna Cell id
    :param key_id: Key id token for OpenCellId
    :return: Tuple Lat, Long returned from OpenCellId
    """

    url = BASE_URL + "?key=" + key_id + "&mnc=" + str(mnc) + "&mcc=" + str(mcc) + "&cellid=" + str(cid) + "&lac=" + str(
        lac) + "&format=json"
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            return json["lat"], json["lon"]
        except:
            return None, None
    else:
        return None, None


def update_antennas_localization(max_number_of_queries: int) -> int:
    """
    Search antennas without latitude and logitude data and ask it to OpenCellId
    Recieve a maximum of queries for day.

    :param max_number_of_queries: Max number of queries to make for each call
    :return: Number of antennas updated
    """
    from app.models.antenna import Antenna
    from app.models.carrier import Carrier
    from config import OpenCellIdToken
    global LAST_ID

    if LAST_ID >= Antenna.query.count():
        LAST_ID = 0

    antennas = Antenna.query.filter(Antenna.lat == None, Antenna.lon == None, Antenna.id > LAST_ID).limit(
        max_number_of_queries)

    LAST_ID = LAST_ID + max_number_of_queries

    upload_antennas = 0
    for antenna in antennas:
        carrier = Carrier.query.filter(Carrier.id == antenna.carrier_id).first()
        lat, lon = get_antenna_geolocalization(mcc=carrier.mcc, mnc=carrier.mnc, lac=antenna.lac, cid=antenna.cid,
                                               key_id=OpenCellIdToken.token)
        if lat and lon:
            antenna.lat = lat
            antenna.lon = lon
            db.session.add(antenna)
            try:
                db.session.commit()
                upload_antennas = upload_antennas + 1
            except Exception as e:
                application.logger.error("Error updating antenna id:" + str(antenna.id) + "to database - " + str(e))
                db.session.rollback()
    return upload_antennas
