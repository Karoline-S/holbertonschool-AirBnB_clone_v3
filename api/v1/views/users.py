#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def serve_users():
    """
    GET REQUEST: return json string containing all User objects
    in storage

    POST REQUEST: creates a new User from request and returns new
    object's dict in JSON string

    ERROR HANDLING: throws 400 error if 'email' or 'password' key not
    in body response dict, or if body response not a valid json
    """
    if request.method == 'GET':
        all_users_list = []
        all_users_dict = storage.all(User)
        for user_obj in all_users_dict.values():
            all_users_list.append(user_obj.to_dict())
        return jsonify(all_users_list)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")
        if 'email' not in body:
            abort(400, description="Missing email")
        if 'password' not in body:
            abort(400, description="Missing password")

        new_user_attrs = {}
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                new_user_attrs[key] = value
        new_user = User(**new_user_attrs)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def serve_user_from_id(user_id):
    """
    GET REQUEST: returns JSON string containing the user object
    correspondong to user_id

    DELETE REQUEST: deletes a user object with corresponding user_id from
    storage and returns an emtpy dict

    PUT REQUEST: updates a user object with corresponding user_id from
    storage and returns a dict containing updated object

    ERROR HANDLING: throws a 404 error if user_id not found
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    if request.method == 'GET':
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(user_obj)
        storage.save()
        return {}

    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")

        updates_dict = {}
        for k, v in body.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                updates_dict[k] = v
        user_obj.update(**updates_dict)
        user_obj.save()
        return jsonify(user_obj.to_dict())
