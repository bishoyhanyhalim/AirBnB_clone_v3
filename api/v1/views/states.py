#!/usr/bin/python3
""" this is states route for website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_the_list():
    """ this is a method for states """
    all_the_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_the_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states_method(state_id):
    """ this is a method for states """
    state_get = storage.get(State, state_id)
    if state_get is None:
        abort(404)
    return jsonify(state_get.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    """ this is a method for states """
    delete_the_state = storage.get(State, state_id)
    if delete_the_state is None:
        abort(404)
    delete_the_state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_states():
    """ this is a method for states """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    create_the_state = request.get_json()
    obj = State(**create_the_state)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_method(state_id):
    """ this is a method for states """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
