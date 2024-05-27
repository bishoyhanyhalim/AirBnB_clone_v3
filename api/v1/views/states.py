#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    all_list = []

    for obj in storage.all(State).values():
        all_list.append(obj.to_dict())

    return (jsonify(all_list))


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    get_id_state = storage.get(State, state_id)

    if get_id_state is None:
        abort(404)

    return jsonify(get_id_state.to_dict())


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    delete_id_state = storage.get(State, state_id)

    if delete_id_state is None:
        abort(404)

    delete_id_state.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def creates_states():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_create = request.get_json()
    obj = State(**new_create)
    obj.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_states(state_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    update_state = storage.get(State, state_id)

    if update_state is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(update_state, key, value)
    storage.save()

    return jsonify(update_state.to_dict())
