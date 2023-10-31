#!/usr/bin/python3
"""this module is the entry point to the REST API"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(parm):
    """End the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """handles 404 error by returns error object"""
    error_dict = {"error": "Not found"}
    status_code = 404
    return jsonify(error_dict), status_code


if __name__ == '__main__':
    """to be imported directly"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
