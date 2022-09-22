#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def serve_reviews(place_id):
    """
    GET REQUEST: return json string containing all Review objects
    associated with a place_id

    POST REQUEST: creates a new Review from request and returns new
    object's dict in JSON string and 201 status

    ERROR HANDLING:
    404 error: place_id not linked to place
    404 error: user_id not linked to user
    400 error: request body doesn't contain key 'user_id'
    400 error: request body doesn't contain key 'text'
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        all_reviews_list = []
        all_reviews_dict = storage.all(Review)
        for review_obj in all_reviews_dict.values():
            if review_obj.place_id == place_id:
                all_reviews_list.append(review_obj.to_dict())
        return jsonify(all_reviews_list)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")
        if 'user_id' not in body:
            abort(400, description="Missing user_id")
        if 'text' not in body:
            abort(400, description="Missing text")

        new_review_attrs = {}
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                new_review_attrs[key] = value
        new_review_attrs['place_id'] = place_id

        user = storage.get(User, new_review_attrs['user_id'])
        if not user:
            abort(404)

        new_review = Review(**new_review_attrs)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def serve_review_from_id(review_id):
    """
    GET REQUEST: returns JSON string containing the review object
    correspondong to review_id

    DELETE REQUEST: deletes a review object with corresponding rewview_id from
    storage and returns an emtpy dict

    PUT REQUEST: updates a review object with corresponding rewview_id from
    storage and returns a dict containing updated object

    ERROR HANDLING:
    404 error: if review_id not found
    400 error: request body is not a valid JSON
    """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(review_obj)
        storage.save()
        return {}

    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")

        updates_dict = {}
        for k, v in body.items():
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                updates_dict[k] = v
        review_obj.update(**updates_dict)
        review_obj.save()
        return jsonify(review_obj.to_dict())
