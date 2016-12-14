import os

import requests

from app import db, application
from config import Urls, Files

BASE_URL = Urls.BASE_URL_OPENCELLID
LOG_FOLDER = Files.LOGS_FOLDER
LOG_FILE = Files.GEOLOCALIZATION_LOG_FILE


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
    Search antennas without latitude and longitude data and ask it to OpenCellId
    Recieve a maximum of queries for day.

    :param max_number_of_queries: Max number of queries to make for each call
    :return: Number of antennas updated
    """
    from app.models.antenna import Antenna
    from app.models.carrier import Carrier
    from  config import OpenCellIdToken
    from datetime import datetime

    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    upload_antennas = 0
    with open(LOG_FOLDER + "/" + LOG_FILE, "a+") as logfile:
        # Go to the beginning of the file
        logfile.seek(0, 0)
        lines = logfile.readlines()

        # if there is last line
        if lines != []:
            import ast
            last_line = ast.literal_eval(lines[-1])
            last_id = last_line["last_id"]

            # all antennas searched
            if last_id >= Antenna.query.count():
                last_id = 0
                #Borrar log
                logfile.seek(0)
                logfile.truncate()

        # first time
        else:
            last_id = 0

        antennas = Antenna.query.filter(Antenna.lat == None, Antenna.lon == None, Antenna.id > last_id).limit(
            max_number_of_queries)

        # searching for antennas
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
                    application.logger.error(
                        "Error updating antenna id: " + str(antenna.id) + " to database - " + str(e))
                    db.session.rollback()

        # writing log
        last_id += max_number_of_queries
        date = datetime.now().strftime("%H:%M %d/%m/%Y")
        log_line = "'date':'" + str(date) + "', 'last_id':" + str(last_id) + ", 'geolocalizated_antennas':" + str(
            upload_antennas)
        logfile.write("{" + log_line + "}\n")

        application.logger.info("Geolocalization process: " + log_line)

        logfile.close()

    return upload_antennas
