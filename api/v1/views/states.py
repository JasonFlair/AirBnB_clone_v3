#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, abort
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
    all_states = storage.all(State).values()
    for state in all_states:
        state_dict = state.to_dict()
        if state_dict["id"] == state_id:
            return jsonify(state_dict)
    abort(404, "Not found")


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    all_states = storage.all(State).values()
    for state in all_states:
        state_dict = state.to_dict()
        if state_dict["id"] == state_id:
            del all_states[state]
            storage.save()
            return jsonify({})
    abort(404, "Not found")