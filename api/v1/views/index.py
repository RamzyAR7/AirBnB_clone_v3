#!/usr/bin/python3
"""
Script that defines a Flask blueprint resources
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns storage stats"""
    returned_dic = {}
    clss = {"Amenity": "amenities", "City": "cities", "Place": "places",
            "Review": "reviews", "State": "states", "User": "users"}
    for key, value in clss.items():
        returned_dic[value] = storage.count(key)
    return jsonify(returned_dic)
