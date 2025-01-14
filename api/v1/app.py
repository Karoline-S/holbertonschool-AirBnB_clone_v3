#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception=None):
    """remove the current SQLAlchemy Session:"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")),
            threaded=True, debug=True)
