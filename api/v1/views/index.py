#!/usr/bin/python3
"""this module handles the statues code route"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """returns 200 code as JSON object"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by its type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for key, value in classes.items():
        count_dict[key] = storage.count(value)
    return jsonify(count_dict)
