from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Date, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)


class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.foreign_key(User.id), nullable=False)
    car_id = db.Column(db.Integer, db.foreign_key(Car.id), nullable=False)
    pickup_date = db.Column(db.Date, nulllable=False)
    return_date = db.Column(db.Date)
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User', backref=db.backref('rentals', lazy=True))
    car = db.relationship('Car', backref=db.backref('rentals', lazy=True))


