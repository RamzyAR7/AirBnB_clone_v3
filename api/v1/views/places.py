#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_place_of_city(city_id):
    """Retrieves the list of all Places objects of City"""
    city_dict = storage.all("City")
    place_list = []
    try:
        places = city_dict[f"City.{city_id}"].places
    except KeyError:
        abort(404)
    for place in places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves Place object"""
    place_dict = storage.all("Place")
    try:
        return jsonify(place_dict[f"City.{place_id}"].to_dict())
    except KeyError:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """Deletes Place object"""
    places_dict = storage.all("Place")
    try:
        storage.delete(places_dict[f"Place.{place_id}"])
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_places(city_id):
    """Adds Place object"""
    try:
        city = storage.all("City")[f"City.{city_id}"]
    except KeyError:
        abort(404)
    try:
        http_dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    try:
        user_id = http_dic["user_id"]
    except KeyError:
        abort(400, 'Missing user_id')
    user_dict = storage.all("User")
    try:
        user = user_dict[f"User.{user_id}"]
    except KeyError:
        abort(404)
    try:
        name = http_dic["name"]
    except KeyError:
        abort(400, 'Missing name')
    new_place = Place(**http_dic)
    new_place.city_id = city_id
    new_place.user_id = user_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def edit_places(place_id):
    """Edits Place object"""
    not_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    places_dict = storage.all("Place")
    try:
        place = places_dict[f"Place.{place_id}"]
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
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    req = request.get_json()
    if req is None or (
        req.get('states') is None and
        req.get('cities') is None and
        req.get('amenities') is None
    ):
        obj_places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in obj_places.values()])

    places = set()

    if req.get('states'):
        obj_states = {storage.get(State, id) for id in req.get('states')}

        for obj_state in obj_states:
            for obj_city in obj_state.cities:
                for obj_place in obj_city.places:
                    places.add(obj_place)

    if req.get('cities'):
        obj_cities = {storage.get(City, id) for id in req.get('cities')}
        obj_cities.discard(None)
        for obj_city in obj_cities:
            for obj_place in obj_city.places:
                places.add(obj_place)

    if not places:
        places = storage.all(Place).values()

    if req.get('amenities'):
        obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
        conf_places = []
        for place in places:
            conf_places.append(place)
            amenities = place.amenities
            for amenity in obj_am:
                if amenity not in amenities:
                    conf_places.pop(-1)
                    break
        places = conf_places
    places = [obj.to_dict() for obj in places]
    return jsonify(places)
