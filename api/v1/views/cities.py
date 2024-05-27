#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_of_states(state_id):
    """Retrieves the list of all City objects of State"""
    state_dict = storage.all("State")
    city_list = []
    try:
        cities = state_dict[f"State.{state_id}"].cities
    except Exception:
        abort(404)
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(city_id):
    """Retrieves the list of all City objects or one state"""
    city_dict = storage.all("City")
    try:
        return jsonify(city_dict[f"City.{city_id}"].to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_cities(city_id):
    """Deletes City object"""
    cities_dict = storage.all("City")
    try:
        storage.delete(cities_dict[f"City.{city_id}"])
        storage.save()
        return jsonify({})
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_cities(state_id):
    """Adds City object"""
    try:
        state = storage.all("State")[f"State.{state_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    try:
        name = http_dic["name"]
    except KeyError:
        abort(400, 'Missing name')
    new_city = City(**http_dic)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def edit_cities(city_id):
    """Edits City object"""
    not_list = ["id", "state_id", "created_at", "updated_at"]
    cities_dict = storage.all("City")
    try:
        city = cities_dict[f"City.{city_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in http_dic.items():
        if key in not_list:
            pass
        else:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
