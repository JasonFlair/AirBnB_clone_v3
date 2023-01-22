#!/usr/bin/python3
"""users blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.user import User
from models import storage


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """gets user specified"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users", strict_slashes=False)
def get_users():
    """get all users"""
    all_users = storage.all(User).values()
    results = []
    for user in all_users:
        user_dict = user.to_dict()
        results.append(user_dict)
    return jsonify(results)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes user object with the id specified"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """creates user object"""
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if not data:
        # if data is not gotten from the request.get_json()
        abort(400, "Not a JSON")

    user = User(**data)
    # the init handles the created_at and updated_at data
    storage.new(user)
    storage.save()
    return make_response(jsonify(data), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates user object"""
    data = request.get_json()
    if not data:
        # if data is not gotten from the request.get_json()
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
