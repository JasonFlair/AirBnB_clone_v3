#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    error_dict = {"error": "Not found"}
    if request.path.startswith('/api/'):
        return jsonify(error_dict)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT') or 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
