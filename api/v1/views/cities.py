#!/usr/bin/python3
"""Manages RESTful API requests for City objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from api.v1.views.base_actions import REST_actions


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_city(state_id):
    """Returns City objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = list(map(lambda city: city.to_dict(), state.cities))
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """returns a City object by its (Id)"""
    city = REST_actions.get_by_id(City, city_id)
    if city.get('status code') == 404:
        abort(404)
    return jsonify(city.get('object dict'))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a City object by its (Id)"""
    delete_response = REST_actions.delete(City, city_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """creates a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_body = request.get_json()

    if request_body is None:
        abort(400, "Not a JSON")
    if not request_body.get('name'):
        abort(400, "Missing name")
    new_city = City(name=request_body.get('name'), state_id=state_id)
    post_response = REST_actions.post(new_city)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """ updates the City object by its (Id) """
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    args_to_ignore = ['id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        City, city_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')
