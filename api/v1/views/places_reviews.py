#!/usr/bin/python3
"""places blueprint"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models import storage
from werkzeug.exceptions import BadRequest


@app_views.route("places/<place_id>/reviews", methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """gets all reviews in a city"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_of_reviews = []
    for review in place.reviews:
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """gets review specified"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes review object with the id specified"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates review object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "text" not in data:
        abort(400, description="Missing text")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data.update({"place_id": place_id})

    review = Review(**data)
    # the init handles the created_at and updated_at data
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates review object"""
    try:
        review = storage.get(Review, review_id)

        if not review:
            abort(404)

        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    except BadRequest:
        abort(400, description="Not a JSON")

