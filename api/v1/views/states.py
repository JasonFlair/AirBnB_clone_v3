#!/usr/bin/python3
"""state blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
def get_states():
    all_states = storage.all(State).values()
    results = []
    for state in all_states:
        state_dict = state.to_dict()
        results.append(state_dict)
    return jsonify(results)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_one_state(state_id):
    """shows state object with the id specified"""
    all_states = storage.all(State).values()
    for state in all_states:
        state_dict = state.to_dict()
        if state_dict["id"] == state_id:
            return jsonify(state_dict)
    abort(404, "Not found")


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes state object with the id specified"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """creates state object"""
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if not data:
        # if data is not gotten from the request.get_json()
        abort(400, "Not a JSON")

    state = State(**data)
    # the init handles the created_at and updated_at data
    storage.new(state)
    storage.save()
    return make_response(jsonify(data), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state object"""
    data = request.get_json()
    if not data:
        # if data is not gotten from the request.get_json()
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
