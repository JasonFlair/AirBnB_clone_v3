#!/usr/bin/python3
"""blueprint index?"""
from api.v1.views import app_views
from flask import jsonify, request, Flask
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

app = Flask(__name__)


@app_views.route("/status")
def return_status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def return_stats():
    amenity_count = storage.count(Amenity)
    place_count = storage.count(Place)
    user_count = storage.count(User)
    state_count = storage.count(State)
    city_count = storage.count(City)
    review_count = storage.count(Review)

    stats_dict = {"amenities": amenity_count, "cities": city_count,
                  "places": place_count, "reviews": review_count,
                  "states": state_count, "users": user_count}
    return jsonify(stats_dict)


@app.errorhandler(404)
@app_views.route("/")
def page_not_found(error):
    print("omoooo")
    error_dict = {"error": "Not found"}
    if request.path.startswith('/api/v1/'):
        return jsonify(error_dict)
