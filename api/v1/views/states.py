#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """Retrieves the list of all State objects or one state"""
    state_dict = storage.all("State")
    if state_id is None:
        states_list = []
        for obj in state_dict.values():
            states_list.append(obj.to_dict())
        return jsonify(states_list)
    try:
        return jsonify(state_dict[f"State.{state_id}"].to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_states(state_id):
    """Deletes State object"""
    state_dict = storage.all("State")
    try:
        storage.delete(state_dict[f"State.{state_id}"])
        storage.save()
        return jsonify({})
    except Exception:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def add_states():
    """Adds State object"""
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    try:
        name = http_dic["name"]
    except KeyError:
        abort(400, 'Missing name')
    new_state = State(**http_dic)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def edit_states(state_id):
    """Edits State object"""
    state_dict = storage.all("State")
    try:
        state = state_dict[f"State.{state_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in http_dic.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
