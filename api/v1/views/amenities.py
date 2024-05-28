#!/usr/bin/python3
"""this is the amenities for show city data on website"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def for_all_amenities():
    """ this is amenities method """
    all_amenit_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_amenit_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ this is amenities method """
    get_all_the_amenity = storage.get(Amenity, amenity_id)
    if get_all_the_amenity is None:
        abort(404)
    return jsonify(get_all_the_amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ this is amenities method """
    amenity_delete = storage.get(Amenity, amenity_id)
    if amenity_delete is None:
        abort(404)
    amenity_delete.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_the_amenity():
    """ this is amenities method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    create_amenity = request.get_json()
    obj = Amenity(**create_amenity)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_the_amenity(amenity_id):
    """ this is amenities method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
