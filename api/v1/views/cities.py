#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """gets all cities for a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_of_cities = []
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    return jsonify(list_of_cities)


@app_views.route("/cities/<city_id>", strict_slashes=False)
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
    """deletes state object"""
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if not data:
        # if data is not gotten from the request.get_json()
        abort(400, "Not a JSON")
    data.update({"state_id": state_id})

    city = City(**data)
    # the init handles the created_at and updated_at data
    storage.new(city)
    storage.save()
    return make_response(jsonify(data), 201)
