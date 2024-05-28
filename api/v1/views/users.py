#!/usr/bin/python3
"""this is the user for show user data on website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_the_all_user():
    """ this is the user method  """
    all_list_data = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_list_data)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_the_user(user_id):
    """ this is the user method  """
    get_all_user = storage.get(User, user_id)
    if get_all_user is None:
        abort(404)
    return jsonify(get_all_user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_user(user_id):
    """ this is the user method  """
    delete_the_user = storage.get(User, user_id)
    if delete_the_user is None:
        abort(404)
    delete_the_user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_obj_user():
    """ this is the user method  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password'not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    create_newUser = request.get_json()
    obj = User(**create_newUser)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def post_user(user_id):
    """ this is the user method  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
