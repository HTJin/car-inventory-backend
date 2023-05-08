from flask import Blueprint, request, jsonify
from ..helpers import token_required, get_images
from ..models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/cars/<fire_token>', methods=['POST'])
@token_required
def create_car(our_user, fire_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    price = request.json['price']
    is_new = request.json['is_new']
    vehicle_type = request.json['vehicle_type']
    fuel_type = request.json['fuel_type']
    image = get_images(make, model, year, color, vehicle_type)
    user_token = fire_token

    car = Car(make, model, year, color, price, is_new,
              vehicle_type, fuel_type, image, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<fire_token>', methods=['GET'])
@token_required
def get_cars(our_user, fire_token):
    owner = fire_token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods=['PUT'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.price = request.json['price']
    car.is_new = request.json['is_new']
    car.vehicle_type = request.json['vehicle_type']
    car.fuel_type = request.json['fuel_type']
    car.image = get_images(car.make, car.model, car.year,
                           car.color, car.vehicle_type)

    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>/remove', methods=['POST', 'DELETE'])
@token_required
def delete_car(id):
    car = Car.query.get(id)

    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
