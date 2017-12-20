#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', strict_slashes=False)
def all_states():
    """Return list of all states"""
    all_states = storage.all("State")
    return jsonify([ obj.to_dict() for obj in all_states.values() ])

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    """Add state to states"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': "Not a JSON"}), 400
    name = data.get('name', None)
    if not name:
        return jsonify({'Error': "Missing name"}), 400

    # this State already exists. Just update State with new data
    for state in storage.all("State").values():
        if state.name == name:
            setattr(state, "name", name)
            state.save()
            return jsonify(state.to_dict()), 200

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def manipulate_state(state_id):
    """GET/UPDATE/DELETE State object based off id else raise 400"""

    state = storage.get("State", state_id) # Get State
    if not state:
        abort(404)

    if request.method == 'PUT': # Update State
        data = request.get_json()
        if not data:
            return jsonify({'Error': "Not a JSON"}), 400
        # update attributes
        [setattr(state, key, value) for key, value in data.items() \
                if key not in ["id", "created_at", "updated_at"]]
        state.save()

    if request.method == 'DELETE': # Delete State
        state.delete()
        storage.save()
        return jsonify({}), 200 # DELETE method

    return jsonify(state.to_dict()), 200 # GET, PUT method
