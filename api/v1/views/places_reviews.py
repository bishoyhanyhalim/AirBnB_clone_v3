#!/usr/bin/python3
"""this is the places reviews for show place data on website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_the_reviews(place_id):
    """ this is the place reviews method  """
    review_place = storage.get(Place, place_id)
    if review_place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in review_place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_for_the_review(review_id):
    """ this is the place reviews method  """
    review_place = storage.get(Review, review_id)
    if review_place is None:
        abort(404)
    return jsonify(review_place.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_review(review_id):
    """ this is the place reviews method  """
    review_the_place = storage.get(Review, review_id)
    if review_the_place is None:
        abort(404)
    review_the_place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_new_the_review(place_id):
    """ this is the place reviews method  """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj_for_review = Review(**kwargs)
    obj_for_review.save()
    return (jsonify(obj_for_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_the_review(review_id):
    """ this is the place reviews method  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj_for_review = storage.get(Review, review_id)
    if obj_for_review is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(obj_for_review, key, value)
    storage.save()
    return jsonify(obj_for_review.to_dict())
