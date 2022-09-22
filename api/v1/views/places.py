#!/usr/bin/python3
""" create a new view for City objects that handles all default                  RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
import models
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    all_places_dict = storage.all(Place)
    places_list = []
    for place in all_places_dict.values():
        if city_id == place.city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_get(place_id):
    """ Retrieves a place object based on given id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """ Deletes a place object based on given id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """ Adds a place to a given city id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        content = request.json
        if 'name' not in content:
            abort(400, "Missing name")
        if 'user_id' not in content:
            abort(400, "Missing user_id")
        user_id = storage.get(User, content['user_id'])
        if user_id is None:
            abort(404)
        new_place = Place(name=content['name'],city_id=city_id,
                          user_id=content['user_id'])
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """ Updates a place based on given id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        content = request.json
        new_dict = {}
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for k, v in content.items():
            if k not in ignore:
                new_dict[k] = v
        place.update(**new_dict)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(400, "Not a JSON")
