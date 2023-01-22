#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest


@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """gets amenity specified"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """get all amenities"""
    all_amenities = storage.all(Amenity).values()
    results = []
    for amenity in all_amenities:
        amenity_dict = amenity.to_dict()
        results.append(amenity_dict)
    return jsonify(results)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity object with the id specified"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates amenity object"""
    try:
        data = request.get_json()
    except BadRequest:
        return abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    # the init handles the created_at and updated_at data
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates state object"""
    try:
        data = request.get_json()
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        ignore = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    except BadRequest:
        abort(400, description="Not a JSON")
