#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


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
            all_amenities_list.append(amenity_obj.to_dict())
        return jsonify(all_amenities_list)

    if request.method == 'POST':
        body = request.get_json()
        if body:
            if 'name' in body:
                new_amenity_attrs = {}
                for key, value in body.items():
                    if key not in ['id', 'created_at', 'udpated_at']:
                        new_amenity_attrs[key] = body[key]
                new_amenity = Amenity(**new_amenity_attrs)
                new_amenity.save()
                return jsonify(new_amenity.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def serve_amenity_from_id(amenity_id):
    """
    GET REQUEST: returns JSON string containing the amenity object
    correspondong to amenity_id

    DELETE REQUEST: deletes an amenity object with corresponding amenity_id
    from storage and returns an emtpy dict

    PUT REQUEST: updates an amenity object with corresponding amenity_id from
    storage and returns a dict containing updated object

    ERROR HANDLING: throws a 404 error if amenity_id not found
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    print(amenity_obj)
    if amenity_obj:
        if request.method == 'GET':
            print(amenity_obj.to_dict())
            return jsonify(amenity_obj.to_dict())

        if request.method == 'DELETE':
            storage.delete(amenity_obj)
            storage.save()
            return {}

        if request.method == 'PUT':
            updates_dict = {}
            body = request.get_json()
            if body:
                for k, v in body.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        updates_dict[k] = v
                amenity_obj.update(**updates_dict)
                amenity_obj.save()
                return jsonify(amenity_obj.to_dict())
            else:
                abort(400, description="Not a JSON")

    else:
        abort(404)
