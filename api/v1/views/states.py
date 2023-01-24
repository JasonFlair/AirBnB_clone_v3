#!/usr/bin/python3
"""state blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    all_states = storage.all(State).values()
    results = []
    for state in all_states:
        state_dict = state.to_dict()
        results.append(state_dict)
    return jsonify(results)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_one_state(state_id):
    """shows state object with the id specified"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_dict = state.to_dict()
    return jsonify(state_dict)


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
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    state = State(**data)
    # the init handles the created_at and updated_at data
    state.save()
    """calls the save function on itself, from basemodel
    which creates a new instance and saves it
    check user for a less confusing method of saving"""
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state object"""
    try:
        data = request.get_json()
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        ignore = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    except BadRequest:
        abort(400, description="Not a JSON")
