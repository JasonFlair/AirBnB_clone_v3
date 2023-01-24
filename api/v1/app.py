#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """teardown storage after use"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """error 404 handler"""
    error_dict = {"error": "Not found"}
    if request.path.startswith('/api/'):
        return make_response(jsonify(error_dict), 404)


if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
