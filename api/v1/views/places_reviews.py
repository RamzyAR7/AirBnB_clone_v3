#!/usr/bin/python3
""" script that defines a Flask blueprint resources"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_review_of_place(place_id):
    """Retrieves the list of all Reviews objects of Place"""
    place_dict = storage.all("Place")
    review_list = []
    try:
        reviews = place_dict[f"Place.{place_id}"].reviews
    except KeyError:
        abort(404)
    for review in reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves Place object"""
    review_dict = storage.all("Review")
    try:
        return jsonify(review_dict[f"Review.{review_id}"].to_dict())
    except KeyError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """Deletes Review object"""
    review_dict = storage.all("Review")
    try:
        storage.delete(review_dict[f"Review.{review_id}"])
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review(place_id):
    """Adds Review object"""
    try:
        place = storage.all("Place")[f"Place.{place_id}"]
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
        text = http_dic["text"]
    except KeyError:
        abort(400, 'Missing text')
    new_review = Review(**http_dic)
    new_review.place_id = place_id
    new_review.user_id = user_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def edit_reviews(review_id):
    """Edits Review object"""
    not_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review_dict = storage.all("Review")
    try:
        review = review_dict[f"Review.{review_id}"]
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
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
