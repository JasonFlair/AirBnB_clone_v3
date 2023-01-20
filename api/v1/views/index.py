#!/usr/bin/python3
"""blueprint index?"""
import api.v1.views
from json import jsonify

app_views = api.v1.views.app_views


@app_views.route("/status")
def return_status():
    return jsonify({"status": "OK"})
