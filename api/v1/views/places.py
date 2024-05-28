#!/usr/bin/python3
"""this is the place for show city data on website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_city_all_places(city_id):
    """ this is the place method  """
    get_city_place = storage.get(City, city_id)
    if get_city_place is None:
        abort(404)
    places = [obj.to_dict() for obj in get_city_place.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_all_the_place(place_id):
    """ this is the place method  """
    get_place = storage.get(Place, place_id)
    if get_place is None:
        abort(404)
    return jsonify(get_place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_place(place_id):
    """ this is the place method  """
    delete_the_place = storage.get(Place, place_id)
    if delete_the_place is None:
        abort(404)
    delete_the_place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_the_place(city_id):
    """ this is the place method  """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj = Place(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_the_place(place_id):
    """ this is the place method  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    the_obj = storage.get(Place, place_id)
    if the_obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(the_obj, key, value)
    storage.save()
    return jsonify(the_obj.to_dict())
