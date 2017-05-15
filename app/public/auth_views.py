from flask_cors import cross_origin

from app import application, socketio
from flask_socketio import emit, join_room, close_room
from flask import request
import uuid

thread = None


def background_thread():
    """send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/gencode')


@application.route("/auth", methods=["POST"])
@cross_origin()
def request_auth():
    from flask import jsonify
    request.namespace = "/gencode"
    body = request.json
    msg = {"data": {
        "op": 'authdone',
        "accessToken": body["access_token"]
    }}
    uuid = body["uuid"]
    emit("message", msg, room=uuid)
    close_room(uuid)
    return jsonify({"status":"OK"}), 200


@socketio.on('connect', namespace='/gencode')
def socket_connect():
    print("connected")
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('connection')


@socketio.on('disconnect', namespace='/gencode')
def socket_disconnect():
    print('disconencted')


@socketio.on('message', namespace='/gencode')
def socket_message(message):
    from flask import json
    obj = json.loads(message)
    if (obj["op"] == 'hello'):
        uuid_token = str(uuid.uuid4())

        join_room(uuid_token)
        hello = { "data": {
            "op": 'hello',
            "token": uuid_token
        }}

        print(hello)
        emit('message', hello)