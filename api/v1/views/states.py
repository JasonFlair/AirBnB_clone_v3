#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage
from datetime import datetime
import json
import uuid


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
            storage.delete(state_dict)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404, "Not found")


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if 'name' not in data:
        abort(make_response(jsonify(message="Missing name"), 400))
    if not isinstance(data, dict):
        abort(400, "Not a JSON")

    data["__class__"] = "State"
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    data["id"] = str(uuid.uuid4())

    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(data)
