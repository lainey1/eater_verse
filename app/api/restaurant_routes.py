from flask import Blueprint, jsonify, request
from app.models import Restaurant, db

restaurant_routes = Blueprint('restaurants', __name__)


@restaurant_routes.route('/')
def restaurants():
    """
    Query for all restaurants and returns them in a list of restaurant dictionaries
    """
    restaurants = Restaurant.query.all()
    return {'restaurants': [restaurant.to_dict() for restaurant in restaurants]}


@restaurant_routes.route('/<int:id>', methods=['GET', 'DELETE'])
def restaurant(id):
    """
    Handle GET and DELETE requests for a restaurant by ID.
    - GET: Query for a restaurant by ID and return it as a dictionary.
    - DELETE: Delete a restaurant by ID from the database.
    """
    restaurant = Restaurant.query.get(id)

    if not restaurant:
        return {'error': f'Restaurant with ID {id} not found.'}, 404

    if request.method == 'GET':
        return restaurant.to_dict(), 200

    if request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant with ID {id} deleted successfully.'}, 200
