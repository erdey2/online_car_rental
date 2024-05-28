from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import db, Car, User, Rental
from werkzeug.security import generate_password_hash, check_password_hash
from app import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hash_password = generate_password_hash(password)
        user1 = User(username=username, password=hash_password, email=email)

        db.session.add(user1)
        db.session.commit()
        flash('registration successful', 'successful')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/cars', methods=['GET', 'POST'])
@login_required
def manage_cars():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        # price_per_day = request.form['price_per_day']

        car = Car(make=make, model=model, year=year)
        # price_per_day = price_per_day
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('manage_cars'))
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


@app.route('/delete_car/<int:car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        flash('car deleted successfully', 'success')
    else:
        flash('car not found', 'danger')
    return redirect(url_for('manage_cars'))


@app.route('/list_cars')
def list_cars():
    cars = Car.query.all()
    return render_template('car_list.html', cars=cars)


@app.route('/car/<int:car_id>')
def car_profile(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_profile.html', car=car)


@app.route('/rentals', methods=['GET', 'POST'])
@login_required
def manage_rentals():
    if request.method == 'POST':
        car_id = request.form['car_id']
        rental_date = request.form['rental_date']

        rental = Rental(user_id=current_user.id, car_id=car_id, rental_date=rental_date)

        car = Car.query.get(car_id)
        car.availability = False

        db.session.add(rental)
        db.session.commit()
        return redirect(url_for('manage_rentals'))
    rentals = Rental.query.filter_by(user_id=current_user.id).all()
    cars = Car.query.filter_by(availability=True).all()
    return render_template('rentals.html', rentals=rentals, cars=cars)
