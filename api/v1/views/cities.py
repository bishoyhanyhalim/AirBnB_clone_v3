#!/usr/bin/python3
"""this is the cities for show city data on website"""
from flask import request, abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_city_list(state_id):
    get_all_state = storage.get(State, state_id)

    if get_all_state is None:
        abort(404)

    all_city_list = []

    for city_obj in storage.all(City).values():
        all_city_list.append(city_obj.to_dict())

    return (jsonify(all_city_list))


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def city_object(city_id):
    get_all_city = storage.get(City, city_id)

    if get_all_city is None:
        abort(404)

    return (jsonify(get_all_city.to_dict()))


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_the_city(city_id):

    get_city = storage.get(City, city_id)

    if get_city is None:
        abort(404)

    get_city.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    get_all_state = storage.get(State, state_id)

    if get_all_state in None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    create_for_city = request.get_json()
    the_create = City(**create_for_city)
    the_create.state_id = get_all_state.id
    the_create.save()

    return (jsonify(the_create.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
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
