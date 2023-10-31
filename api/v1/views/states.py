#!/usr/bin/python3
"""Manages all  RESTful API requests for state object"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from api.v1.views.base_actions import REST_actions


@app_views.route('/states', methods=['GET'])
def get_states():
    """returns all State objects"""
    return jsonify(REST_actions.get(State))


@app_views.route('/states', methods=['POST'])
def post_state():
    """creates a new state"""
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    if not request_body.get('name'):
        abort(400, "Missing name")
    new_state = State(name=request_body.get('name'))
    post_response = REST_actions.post(new_state)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """returns a State object its (Id)"""
    state = REST_actions.get_by_id(State, state_id)
    if state.get('status code') == 404:
        abort(404)
    return jsonify(state.get('object dict'))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a State object its (Id)"""
    delete_response = REST_actions.delete(State, state_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ updates a State object by its (Id) """
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Not a JSON'}), 400

    args_to_ignore = ['id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        State, state_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')
