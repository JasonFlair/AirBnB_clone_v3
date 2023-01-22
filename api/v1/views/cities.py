#!/usr/bin/python3
"""city blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models import storage
from werkzeug.exceptions import BadRequest


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """gets all cities for a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_of_cities = []
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    return jsonify(list_of_cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """gets city specified"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes city object with the id specified"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates state object"""
    try:
        data = request.get_json()
    except BadRequest:
        return abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    data.update({"state_id": state_id})

    city = City(**data)
    # the init handles the created_at and updated_at data
    storage.new(city)
    storage.save()
    return make_response(jsonify(data), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates city object"""
    try:
        data = request.get_json()
    except BadRequest:
        return abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)