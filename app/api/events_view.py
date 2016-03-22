import werkzeug
from flask import request
from flask_restful import Resource, reqparse

from . import app


class SaveEvents(Resource):
    def post(self):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

        #args = post_parser.parse_args()
        pass


import zipfile


@app.route("/send_file", methods=['POST'])
def read_events():
    f = request.files['pic']

    z = zipfile.ZipFile(f)
    for name in z.namelist():
        json = z.open(name)
        lines = json.readlines()
        string = ' '.join(str(x) for x in lines)
        print(string)

    return f