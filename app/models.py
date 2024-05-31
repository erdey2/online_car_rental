from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_no = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(100))
    role = db.Column(db.String(50), default='customer')

    def __init__(self, username, password, email, contact_no, address):
        self.username = username
        self.password = password
        self.email = email
        self.contact_no = contact_no
        self.address = address


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, make, model, category, year, price_per_day, availability=True):
        self.make = make
        self.model = model
        self.category = category
        self.year = year
        self.price_per_day = price_per_day
        self.availability = availability

    def is_available(self, start_date, end_date):
        bookings = Booking.query.filter_by(car_id=self.id).all()
        for booking in bookings:
            if booking.start_date <= end_date and booking.end_date >= start_date:
                return False
            return True


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    car = db.relationship('Car', backref=db.backref('bookings', lazy=True))


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey(Car.id), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today())
    end_date = db.Column(db.Date)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_time = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User', backref=db.backref('rentals', lazy=True))
    car = db.relationship('Car', backref=db.backref('rentals', lazy=True))
