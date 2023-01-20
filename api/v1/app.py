#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT') or 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
