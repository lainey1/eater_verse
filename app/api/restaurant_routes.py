from datetime import datetime

import pytz
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app.forms import RestaurantForm
from app.models import Restaurant, RestaurantImage, Review, db

from ..constants import POPULAR_CUISINES, TIME_CHOICES

restaurant_routes = Blueprint('restaurants', __name__)

# A function to convert WTForms fields to JSON
def form_to_json(form):
    fields = {}
    for field_name, field in form._fields.items():
        fields[field_name] = {
            "type": field.type,
            "label": field.label.text,
            "validators": [v.__class__.__name__ for v in field.validators],
            "choices": getattr(field, 'choices', None),  # For SelectField
            "default": field.default,
        }
    return fields

@restaurant_routes.route('/form-schema', methods=['GET'])
def get_form_schema():
    form = RestaurantForm()
    return jsonify(form_to_json(form))



@restaurant_routes.route('/constants')
def get_constants():
    # Get timezone choices from pytz
    timezone_choices = [(tz, tz.replace('_', ' '))
                       for tz in pytz.common_timezones_set
                       if 'America' in tz or 'US' in tz or 'Pacific' in tz]
    timezone_choices.sort()  # Sort alphabetically

    return {
        'time_choices': TIME_CHOICES,
        'popular_cuisines': POPULAR_CUISINES,
        'timezone_choices': timezone_choices
    }

@restaurant_routes.route('/')
def restaurants():
    """
    Query for all restaurants and return them in a list of restaurant dictionaries.
    """
    restaurants = Restaurant.query.all()

    restaurant_data_list = []

    for restaurant in restaurants:
        # Fetch aggregated review data for each restaurant
        review_stats = (
            db.session.query(
                func.count(Review.id).label("reviewCount"),
                func.avg(Review.stars).label("avgStarRating")
            )
            .filter(Review.restaurant_id == restaurant.id)
            .first()
        )

        # Fetch the preview image for the restaurant
        preview_image = RestaurantImage.query.filter_by(restaurant_id=restaurant.id, is_preview=True).first()
        preview_image_url = preview_image.url if preview_image else None

        # Convert the restaurant to a dictionary
        restaurant_data = restaurant.to_dict()

        # Add review stats and preview image to the restaurant data
        restaurant_data['reviewStats'] = {
            "reviewCount": review_stats.reviewCount or 0,
            "avgStarRating": float(review_stats.avgStarRating or 0),
        }
        restaurant_data['previewImage'] = preview_image_url

        restaurant_data_list.append(restaurant_data)

    return {'restaurants': restaurant_data_list}




@restaurant_routes.route('/owner/<int:owner_id>')
def restaurants_by_owner(owner_id):
    """
    Query restaurants by owner ID and return a list of dictionaries,
    where each dictionary represents a restaurant with aggregated review data.
    """
    restaurants_by_owner = Restaurant.query.filter_by(owner_id=owner_id).all()

    if not restaurants_by_owner:
        return {'error': f'No restaurants with an owner by ID {owner_id} found.'}, 404

    restaurant_data_list = []

    for restaurant in restaurants_by_owner:
        # Fetch aggregated review data for each restaurant
        review_stats = (
            db.session.query(
                func.count(Review.id).label("reviewCount"),
                func.avg(Review.stars).label("avgStarRating")
            )
            .filter(Review.restaurant_id == restaurant.id)  # Using the current restaurant's ID
            .first()
        )

        # Convert the restaurant to a dictionary
        restaurant_data = restaurant.to_dict()

        # Add review stats to the restaurant data
        restaurant_data['reviewStats'] = {
            "reviewCount": review_stats.reviewCount or 0,
            "avgStarRating": float(review_stats.avgStarRating or 0),
        }

        restaurant_data_list.append(restaurant_data)

    return {'restaurants': restaurant_data_list}



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
        # Fetch aggregated review data for the restaurant
        review_stats = (
            db.session.query(
                func.count(Review.id).label("reviewCount"),
                func.avg(Review.stars).label("avgStarRating")
            )
            .filter(Review.restaurant_id == id)
            .first()
        )

        # Fetch images for the restaurant
        restaurant_images = RestaurantImage.query.filter_by(restaurant_id=restaurant.id).all()
        images = [image.to_dict() for image in restaurant_images]

        # Convert the restaurant to a dictionary and add review stats
        restaurant_data = restaurant.to_dict()
        restaurant_data['reviewStats'] = {
            "reviewCount": review_stats.reviewCount or 0,
            "avgStarRating": float(review_stats.avgStarRating or 0),
        }
        restaurant_data['images'] = images

        return restaurant_data, 200

    if request.method == 'DELETE':
        # Check if the current user is the owner of the restaurant
        if restaurant.owner_id != current_user.id:
            return {'error': 'You are not authorized to delete this restaurant.'}, 403

        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant with ID {id} deleted successfully.'}, 200



@restaurant_routes.route('/new', methods=['POST'])
@login_required
def create_restaurant():
    """
    Query to add a restaurant to the DB using either JSON or Form data
    """

    if request.is_json:
        # Handle JSON input (from Postman)
        data = request.get_json()

        try:
            new_restaurant = Restaurant(
                owner_id=current_user.id,
                name=data['name'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                country=data['country'],
                phone_number=data.get('phone_number'),
                email=data.get('email'),
                website=data.get('website'),
                cuisine=data.get('cuisine'),
                price_point=data.get('price_point'),
                description=data.get('description'),
                hours=data['hours']  # Directly assign hours from the JSON
            )

            db.session.add(new_restaurant)
            db.session.commit()

            return jsonify(new_restaurant.to_dict()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        # Handle form input (for Flask form later)
        form = RestaurantForm()
        form['csrf_token'].data = request.cookies['csrf_token']

        if form.validate_on_submit():
            print("Form has been submitted and validated.")
            print(form.monday_open.data, form.monday_close.data)
            try:
                new_restaurant = Restaurant(
                    owner_id=current_user.id,
                    name=form.name.data,
                    address=form.address.data,
                    city=form.city.data,
                    state=form.state.data,
                    country=form.country.data,
                    phone_number=form.phone_number.data,
                    email=form.email.data,
                    website=form.website.data,
                    cuisine=form.cuisine.data,
                    price_point=int(form.price_point.data),
                    description=form.description.data,
                    timezone=form.timezone,
                    hours={
                        "Monday": [form.monday_open.data, form.monday_close.data],
                        "Tuesday": [form.tuesday_open.data, form.tuesday_close.data],
                        "Wednesday": [form.wednesday_open.data, form.wednesday_close.data],
                        "Thursday": [form.thursday_open.data, form.thursday_close.data],
                        "Friday": [form.friday_open.data, form.friday_close.data],
                        "Saturday": [form.saturday_open.data, form.saturday_close.data],
                        "Sunday": [form.sunday_open.data, form.sunday_close.data],
                    }
                )


                db.session.add(new_restaurant)
                db.session.commit()

                return jsonify(new_restaurant.to_dict()), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"errors": form.errors}), 400


# Update a restaurant
@restaurant_routes.route('/<int:restaurant_id>/edit', methods=['PUT'])
@login_required
def update_restaurant(restaurant_id):
    """
    Update a restaurant by ID
    """
    # Fetch the restaurant by ID
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'message': 'Restaurant not found'}), 404

    # Check if the current user is the owner
    if restaurant.owner_id != current_user.id:
        return jsonify({'message': 'You are not authorized to update this restaurant. Please log in as the owner to update this restaurant.'}), 403

    # Get data from the request
    data = request.get_json()
    # print(data)

    # Validate required fields
    required_fields = ['name', 'address', 'city', 'state', 'country', 'hours']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    # Update the restaurant fields
    restaurant.name = data['name']
    restaurant.address = data['address']
    restaurant.city = data['city']
    restaurant.state = data['state']
    restaurant.country = data['country']
    restaurant.phone_number = data.get('phone_number')
    restaurant.email = data.get('email')
    restaurant.website = data.get('website')
    restaurant.cuisine = data.get('cuisine')
    restaurant.price_point = data.get('price_point')
    restaurant.description = data.get('description')
    restaurant.timezone = data.get('timezone')
    restaurant.hours = data['hours']

    # Save changes to the database
    db.session.commit()

    return jsonify({'message': 'Restaurant updated successfully', 'restaurant': restaurant.to_dict()}), 200
