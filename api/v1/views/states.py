#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def access_states():
    """
    GET REQUEST: return json string containing all State objects
    in storage

    POST REQUEST: creates a new State from request and returns new
    object's dict in JSON string

    ERROR HANDLING: throws 400 error if 'name' key not in body response
    dict, or body response not a valid json
    """
    if request.method == 'GET':
        all_states_list = []
        all_states_dict = storage.all(State)
        for state_obj in all_states_dict.values():
            all_states_list.append(state_obj.to_dict())
        return jsonify(all_states_list)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")

        if 'name' in not body:
            abort(400, description="Missing name")

        new_state_attrs = {}
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                new_state_attrs[key] = value
        new_state = State(**new_state_attrs)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
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
    if not state_obj:
        abort(404)

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(state_obj)
        storage.save()
        return {}

    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")

        updates_dict = {}
        for k, v in body.items():
            if k not in ['id', 'created_at', 'updated_at']:
                updates_dict[k] = v
        state_obj.update(**updates_dict)
        state_obj.save()
        return jsonify(state_obj.to_dict())
