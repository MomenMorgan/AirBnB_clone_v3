#!/usr/bin/python3
"""Manages the RESTfull api requests for users"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from api.v1.views.base_actions import REST_actions


@app_views.route('/users', methods=['GET'])
def get_users():
    """returns all user object"""
    return jsonify(REST_actions.get(User))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """returns the user object using (Id)"""
    user = REST_actions.get_by_id(User, user_id)
    if user.get('status code') == 404:
        abort(404)
    return jsonify(user.get('object dict'))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes the user object using the (Id)"""
    delete_response = REST_actions.delete(User, user_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def post_user():
    """Creates a new user"""
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('email'):
        return jsonify({'error': 'Missing email'}), 400
    if not request_body.get('password'):
        return jsonify({'error': 'Missing password'}), 400
    new_user = User(**request_body)
    post_response = REST_actions.post(new_user)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """ Add updates to use oject using (Id)"""
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    args_to_ignore = ['id', 'created_at', 'updated_at', 'email']
    put_response = REST_actions.put(
        User, user_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')
