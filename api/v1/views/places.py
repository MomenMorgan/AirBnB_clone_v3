#!/usr/bin/python3
"""Manages the RESTful API requests to Place objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from api.v1.views.base_actions import REST_actions


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """returns a Place object by its (Id)"""
    place = REST_actions.get_by_id(Place, place_id)
    if place.get('status code') == 404:
        abort(404)
    return jsonify(place.get('object dict'))


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """returns the Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = list(map(lambda place: place.to_dict(), city.places))
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes the Place object by its (id)"""
    delete_response = REST_actions.delete(Place, place_id)
    if delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """creates a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_body = request.get_json()
    if request_body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if not request_body.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    if not request_body.get('name'):
        return jsonify({'error': 'Missing name'}), 400
    user = storage.get(User, request_body.get('user_id'))
    if user is None:
        abort(404)
    new_place = Place(name=request_body.get('name'), user_id=user.id,
                      city_id=city_id)
    post_response = REST_actions.post(new_place)
    return post_response.get('object dict'), post_response.get('status code')


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ updates a Place object by its (Id) """
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    args_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    put_response = REST_actions.put(
        Place, place_id, args_to_ignore, request_body)
    if put_response.get('status code') == 404:
        abort(404)
    return put_response.get('object dict'), put_response.get('status code')


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """creates a new Place"""

    try:
        request_body = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Not a JSON'}), 400

    all_places = storage.all(Place)
    all_places_dict = {v.city_id: v for k, v in all_places.items()}

    if request_body == {}:
        places = list(map(lambda x: x.to_dict(), all_places.values()))
        return jsonify(places)
    cities_list = []
    states_ids = request_body.get('states')
    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                cities_list.extend(list(map(lambda s: s.id, state.cities)))
    cities_ids = request_body.get('cities', [])
    cities_list.extend(cities_ids)
    cities_list = list(set(cities_list))

    filtered_places = []
    for x in cities_list:
        place = all_places_dict.get(x, None)
        if place:
            filtered_places.append(all_places_dict[x])

    amenities_ids = request_body.get('amenities', [])
    print(amenities_ids)
    print(filtered_places)
    if amenities_ids:
        for place in filtered_places:
            place_amenities = list(map(lambda x: x.id, place.amenities))
            if not all(elem in place_amenities for elem in amenities_ids):
                filtered_places.remove(place)
    places_dict = list(map(lambda x: x.to_dict(), filtered_places))
    return jsonify(places_dict)
