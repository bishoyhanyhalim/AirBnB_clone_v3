#!/usr/bin/python3
"""this is the cities for show city data on website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_city_list(state_id):
    """ Gets city method """
    get_all_state = storage.get(State, state_id)
    if get_all_state is None:
        abort(404)
    all_city_list = [obj.to_dict() for obj in get_all_state.cities]
    return jsonify(all_city_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city_object(city_id):
    """ Gets city method """
    city_show_all = storage.get(City, city_id)
    if city_show_all is None:
        abort(404)
    return jsonify(city_show_all.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_city(city_id):
    """ Gets city method """
    city_show_all = storage.get(City, city_id)
    if city_show_all is None:
        abort(404)
    city_show_all.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Gets city method """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    create_new_city = request.get_json()
    obj = City(**create_new_city)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Gets city method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
