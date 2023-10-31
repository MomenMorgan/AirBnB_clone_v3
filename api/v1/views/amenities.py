#!/usr/bin/python3
"""Manages  the RESTful API request to Amenity object"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from api.v1.views.base_actions import REST_actions


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """returns the Amenity objects"""
    amenities = REST_actions.get(Amenity)
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """returns ths Amenity object by its (Id)"""
    amenity = REST_actions.get_by_id(Amenity, amenity_id)
    if amenity.get('status code') == 404:
        abort(404)
    return jsonify(amenity.get('object dict'))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes the Amenity object by its (Id)"""
    delete_response = REST_actions.delete(Amenity, amenity_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """creates a new Amenity"""
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('name'):
        return jsonify({'error': 'Missing name'}), 400
    new_amenity = Amenity(name=request_body.get('name'))
    post_response = REST_actions.post(new_amenity)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ updates the Amenity object by its (Id) """
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    args_to_ignore = ['id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        Amenity, amenity_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')
