#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from json import jsonify


@app_views.route("/status")
def return_status():
    return jsonify({"status": "OK"})
