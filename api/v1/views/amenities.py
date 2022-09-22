#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def serve_amenities():
    """
    GET REQUEST: return json string containing all Amenity objects
    in storage

    POST REQUEST: creates a new Amenity from request and returns new
    object's dict in JSON string

    ERROR HANDLING: throws 400 error if 'name' key not in body response
    dict, or body response not a valid json
    """
    if request.method == 'GET':
        all_amenities_list = []
        all_amenities_dict = storage.all(Amenity)
        for amenity_obj in all_amenities_dict.values():
            all_amenities_list.append(state_obj.to_dict())
        return jsonify(all_states_list)
    if request.method == 'POST':
        if request.get_json():
            body = request.get_json()
            if 'name' in body:
                new_state_name = body['name']
                new_state = State(name=new_state_name)
                new_state.save()
                return jsonify(new_state.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def access_state_from_id(state_id):
    """
    GET REQUEST: returns JSON string containing the state object
    correspondong to state_id

    DELETE REQUEST: deletes a state object with corresponding state_id from
    storage and returns an emtpy dict

    PUT REQUEST: updates a state object with corresponding state_id from
    storage and returns a dict containing updated object

    ERROR HANDLING: throws a 404 error if state_id not found
    """
    state_obj = storage.get(State, state_id)
    if state_obj:
        if request.method == 'GET':
            print(state_obj.to_dict())
            return jsonify(state_obj.to_dict())

        if request.method == 'DELETE':
            storage.delete(state_obj)
            models.storage.save()
            return {}

        if request.method == 'PUT':
            updates_dict = {}
            if request.get_json():
                print("we have a request")
                for k, v in request.get_json().items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        state_obj.update(v)
#                    print("looping over request items")
#                    updates_dict[k] = v
#                    print("our new dict is: {}".format(updates_dict))
#                    state_obj.update("hello")
#                    updates_dict = {}
                state_obj.save()
                return jsonify(state_obj.to_dict())
            else:
                abort(400, description="Not a JSON")

    else:
        abort(404)