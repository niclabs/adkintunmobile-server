import os

from flask import request

from app import application
from config import Files

STATIC_FILES_FOLDER = Files.STATIC_FILES_FOLDER
FILES_FOLDER = Files.FILES_FOLDER


@application.route("/speedtest/", methods=["POST"])
def speedtest_post():
    return upload_speedtest()


@application.route("/speedtest/<int:mo_size>", methods=["GET"])
def speedtest_get(mo_size):
    if mo_size > 100:
        return "File too big", 413
    return download_speedtest(mo_size)


def upload_speedtest():
    b = request.data
    return "OK", 200


def download_speedtest(mo_size):
    return get_binary_file(mo_size)


def get_binary_file(mo_size):
    if not os.path.exists(STATIC_FILES_FOLDER + "/" + FILES_FOLDER):
        os.makedirs(STATIC_FILES_FOLDER + "/" + FILES_FOLDER)

    filename = FILES_FOLDER + "/" + str(mo_size) + "Mo.dat"
    try:
        return application.send_static_file(filename)
    except:
        create_random_binary_file(mo_size)
        return get_binary_file(mo_size)


def create_random_binary_file(mbytes):
    bytes = mbytes * (1024 ** 2)
    filepath = STATIC_FILES_FOLDER + "/" + FILES_FOLDER + "/" + str(mbytes) + "Mo.dat"
    with open(filepath, "wb") as fout:
        fout.write(os.urandom(bytes))
    return fout


@application.route("/status/", methods=['GET'])
def get_server_status():
    return "OK", 200


@application.route("/active_servers/", methods=['GET'])
def mifun():
    from flask import jsonify
    return jsonify({'data': [{'added': 'Wed, 12 Oct 2016 19:09:39 GMT', 'country': 'Chile', 'name': 'Dev Niclabs',
                              'host': 'http://dev.niclabs.cl', 'port': '80'}
                             ]})


# Suggested urls list for connectivity test
@application.route("/recommended_sites/", methods=['GET'])
def recommended_sites():
    from flask import jsonify
    return jsonify({'data': ['google.cl', 'youtube.com', 'biobiochile.cl', 'emol.com', 'lun.com', 'facebook.com',
                             'wikipedia.org', 'uchile.cl', 'niclabs.cl', 't13.cl']})
