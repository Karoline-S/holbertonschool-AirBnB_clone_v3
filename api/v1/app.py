from flask import Flask
from models import storage
from os import getenv
import api.v1.views from app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown.appcontext
def close_session(exception=None):
    """ends the sql alchemy session"""
    storage.close()

if getenv(HBNB_API_HOST):
    HOST = getenv(HBNB_API_HOST)
else:
    HOST = "0.0.0.0"

if getenv(HBNB_API_PORT):
    PORT = HBNB_API_PORT
else:
    PORT = 5000

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
