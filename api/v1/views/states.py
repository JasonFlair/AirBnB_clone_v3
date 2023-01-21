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
            del all_states[state]
            storage.save()
            return jsonify({})
    abort(404, "Not found")


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if 'name' not in data:
        abort(make_response(jsonify(message="Missing name"), 400))
    else:
        try:
            json_data = json.loads(data)
            # check that data is in valid JSON format

            json_data["__class__"] = "State"
            json_data["created_at"] = datetime.now()
            json_data["updated_at"] = datetime.now()
            json_data["id"] = str(uuid.uuid4())

            storage.new(json_data)
            storage.save()
            return json_data
        except json.decoder.JSONDecodeError as e:
            # Data is not in valid JSON format
            abort(400, "Not a JSON")

