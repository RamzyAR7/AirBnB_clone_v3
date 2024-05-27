#!/usr/bin/python3
"""Script that starts a Flask web application"""
from os import getenv
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_appcontext(*args):
    """After each request remove current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')
    if HOST is None:
        HOST = '0.0.0.0'
    if PORT is None:
        PORT = 5000
    app.run(host=HOST, port=PORT, threaded=True)
