#!/usr/bin/python3
"""places blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from werkzeug.exceptions import BadRequest


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """gets all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    list_of_places = []
    for place in city.places:
        list_of_places.append(place.to_dict())
    return jsonify(list_of_places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """gets place specified"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes place object with the id specified"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates a place object"""
    try:
        place_data = request.get_json()
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        if 'user_id' in place_data:
            user_id = place_data['user_id']
            user = storage.get(User, user_id)
            if not user:
                abort(404)
        if 'name' not in place_data:
            abort(400, "Missing name")
        if 'user_id' not in place_data:
            abort(400, "Missing user_id")

        place_data.update({"city_id": city_id})

        new_place = Place(**place_data)
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)
    except BadRequest:
        abort(400, "Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        place_data = request.get_json()
        for k, v in place_data.items():
            if k not in ['id', 'user_id',
                         'created_at', 'updated_at']:
                setattr(place, k, v)

        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    except BadRequest:
        abort(400, "Not a JSON")
