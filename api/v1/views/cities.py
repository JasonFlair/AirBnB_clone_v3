#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """gets all cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_of_cities = []
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    return jsonify(list_of_cities)


