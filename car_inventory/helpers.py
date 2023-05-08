from flask import request, jsonify, json
from functools import wraps
from .models import User
import secrets
import decimal
import requests
import os
import inspect


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
        elif 'token' in request.form:
            token = request.form['token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            our_user = User.query.filter_by(token=token).first()
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        if 'our_user' in inspect.signature(flask_function).parameters:
            return flask_function(our_user, *args, **kwargs)
        else:
            return flask_function(*args, **kwargs)
    return decorated


def get_images(make, model, year, color, vehicle_type):
    url = "https://bing-image-search1.p.rapidapi.com/images/search"
    querystring = {"q": f"{year} {make} {model} {color} {vehicle_type}"}
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('API_KEY')}",
        "X-RapidAPI-Host": "bing-image-search1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data['value']['0']['contentUrl']
