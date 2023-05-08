from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import uuid
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String, default='', unique=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, password):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(32)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'email: {self.email} added to Users'


class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.String(4), nullable=True)
    color = db.Column(db.String)
    price = db.Column(db.Numeric(precision=10, scale=2))
    is_new = db.Column(db.Boolean, default=False)
    vehicle_type = db.Column(db.String(15))
    fuel_type = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    user_token = db.Column(db.String, nullable=False)

    def __init__(self, make, model, year, color, price, is_new, vehicle_type, fuel_type, image, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.is_new = is_new
        self.vehicle_type = vehicle_type
        self.fuel_type = fuel_type
        self.image = image
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f'You are now a proud owner of a {self.make} {self.model} from {self.year}! 🙌'


class CarSchema(ma.Schema):
    class Meta:
        fields = ['make', 'model', 'year', 'color', 'price', 'is_new',
                  'vehicle_type', 'fuel_type', 'image']


car_schema = CarSchema()
cars_schema = CarSchema(many=True)
