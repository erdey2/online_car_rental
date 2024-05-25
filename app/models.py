from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, make, model, year, availability=True):
        self.make = make
        self.model = model
        self.year = year
        self.availability = availability


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey(Car.id), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User', backref=db.backref('rentals', lazy=True))
    car = db.relationship('Car', backref=db.backref('rentals', lazy=True))


car1 = Car(make="Toyota", model='Camry', year=2022)
car2 = Car(make="Honda", model='Civic', year=2018)
