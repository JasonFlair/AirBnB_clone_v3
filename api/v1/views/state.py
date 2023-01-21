#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify
from models.base_model import to_dict
from models.state import State
from models import storage


@app_views.route("/states")
def get_states(states):
    results = storage.all(State)
    print(results)
