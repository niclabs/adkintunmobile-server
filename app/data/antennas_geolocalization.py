import requests

BASE_URL = "http://opencellid.org/cell/get"


def get_antenna_geolocalization(mcc: int, mnc: int, lac: int, cid: int, key_id: str, base_url: str) -> tuple:
    """
    Get the geolocalization for an antenna from OpenCellId if exist
    :param mnc: Antenna mnc
    :param mcc: Antenna mcc
    :param lac: Antena local area code
    :param cid: Antenna Cell id
    :param key_id: Key id token for OpenCellId
    :param base_url: OpenCellId url
    :return: Tuple Lat, Long returned from OpenCellId
    """
    url = BASE_URL + "?key=" + key_id + "&mnc=" + str(mnc) + "&mcc="+ str(mcc) + "&cellid=" + str(cid) + "&lac=" + str(lac)+"&format=json"
    r = requests.get(url)
    if r.status_code == 200:
         json = r.json()
         return json["lat"], json["lon"]
    else:
        return None, None


def update_antennas_Localization(max_number_of_queries: int) -> int:
    """
    Search antennas without latitude and logitude data and ask it to OpenCellId
    Recieve a maximum of queries for day.

    :param max_number_of_queries: Max number of queries to make for each call
    :return: Number of antennas updated
    """
    return 0


"""
http://opencellid.org/cell/get?key=579b4655-a318-433c-ad94-b71261313722&mcc=730&mnc=2&lac=55700&cellid=1259355
"""