#!/usr/bin/python3"
"""Manages the  RESTful API requests to Reviews objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from api.v1.views.base_actions import REST_actions


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    """returns the Review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = list(map(lambda review: review.to_dict(), place.reviews))
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """returns the Review object by its (Id)"""
    review = REST_actions.get_by_id(Review, review_id)
    if review.get('status code') == 404:
        abort(404)
    return jsonify(review.get('object dict'))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes the Review object by its (Id)"""
    delete_response = REST_actions.delete(Review, review_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """creates a new Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_body = request.get_json()
    if request_body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    if not request_body.get('text'):
        return jsonify({'error': 'Missing text'}), 400
    user = storage.get(User, request_body.get('user_id'))
    if user is None:
        abort(404)
    new_review = Review(text=request_body.get('text'), user_id=user.id,
                        place_id=place_id)
    post_response = REST_actions.post(new_review)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """ updates the Review object by its (Id) """
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Not a JSON'}), 400

    args_to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        Review, review_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')
