import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.insert(1, dir_path)

import flask
from flask import jsonify, request, redirect, Response
from flask_cors import CORS, cross_origin
import json
import re
import traceback
import base64
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.serving import WSGIRequestHandler
from werkzeug import Response

app = flask.Flask("__main__")
CORS(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5000 per day", "600 per minute"]
)

@app.route("/api/test/", methods=['POST', 'GET'])
@cross_origin(origin='*')
def api_test():
    if request.method == 'GET':
        return "GET request works"

    elif request.method == 'POST':
        json_data = request.get_json()
        if json_data is None : return jsonify({'error': 'Received no input'})

        try:
            print(json_data)
            return json_data
        except Exception as e:
            errorString = "Error in api test. " ; messageString = str(e)
            tracebackString = traceback.format_exc()
            print(f'{errorString}: {messageString}. >>> \n{tracebackString}')

            return jsonify({'error': errorString, 'message': messageString, 'traceback': tracebackString}), 500

if __name__ == '__main__' :
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    from waitress import serve
    app.run(debug=False, host="0.0.0.0", port=5000)