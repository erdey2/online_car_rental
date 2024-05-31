from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from app.models import db, Car, User, Rental, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import app


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        contact_no = request.form['contact_no']
        address = request.form['address']

        hash_password = generate_password_hash(password)
        user = User(username=username, password=hash_password, email=email, contact_no=contact_no, address=address)

        db.session.add(user)
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
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Login successful')
            login_user(user)
            if user.role == 'customer':
                return redirect(url_for('customer_home'))
            else:
                return redirect(url_for('manage_cars'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/customer_home')
def customer_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    cars = Car.query.all()
    return render_template('customer_home.html', user=user, cars=cars)


@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    return render_template('profile.html', user=user)


@app.route('/car_search', methods=['GET', 'POST'])
def car_search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cars = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        cars = Car.query.filter(Car.model.contains(search_term)).all()
    return render_template('car_search.html', cars=cars)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/manage_cars', methods=['GET', 'POST'])
@admin_required
def manage_cars():
    cars = Car.query.all()
    return render_template('manage_cars.html', cars=cars)


@app.route('/car_add', methods=['GET', 'POST'])
@admin_required
def car_add():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        category = request.form['category']
        year = request.form['year']
        price_per_day = request.form['price_per_day']

        # Validate form inputs
        if not make or not model or not year or not category or not price_per_day:
            flash('All fields are required.')
            return redirect(url_for('car_add'))

        # Create a new car instance
        new_car = Car(
            make=make,
            model=model,
            category=category,
            year=int(year),
            price_per_day=float(price_per_day),
            availability=True
        )

        # Add the new car to the database
        db.session.add(new_car)
        db.session.commit()

        flash('Car added successfully!')
        return redirect(url_for('manage_cars'))

    return render_template('car_add.html')


@app.route('/car_edit/<int:car_id>', methods=['GET', 'POST'])
@admin_required
def car_edit(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        car.make = request.form['make']
        car.model = request.form['model']
        car.category = request.form['category']
        car.year = request.form['year']
        car.price_per_day = request.form['price_per_day']

        # Validate form inputs
        if not car.make or not car.model or not car.category or not car.year or not car.price_per_day:
            flash('All fields are required.')
            return redirect(url_for('car_edit', car_id=car_id))

        # Update the car details in the database
        db.session.commit()

        flash('Car details updated successfully!')
        return redirect(url_for('manage_cars'))

    return render_template('car_edit.html', car=car)


@app.route('/car_delete/<int:car_id>', methods=['POST'])
@admin_required
def car_delete(car_id):
    car = Car.query.get_or_404(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        flash('car deleted successfully', 'success')
    else:
        flash('car not found', 'danger')
        return redirect(url_for('manage_cars'))
    return render_template('car_delete.html')


@app.route('/list_cars')
def list_cars():
    cars = Car.query.all()
    return render_template('car_list.html', cars=cars)


@app.route('/car/<int:car_id>')
def car_profile(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_profile.html', car=car)


@app.route('/car_book/<int:car_id>', methods=['GET', 'POST'])
@login_required
def car_book(car_id):
    car = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            return_date = request.form.get('end_date')
        except(ValueError, KeyError):
            flash('Invalid date format or miss date.')
            return redirect(url_for('car_book', car_id=car_id))

        if end_date <= start_date:
            flash('Return date must be after rental date.')
            return redirect(url_for('car_book', car_id=car_id))

        # calculate total cost
        days = (end_date - start_date).days + 1
        total_cost = days * car.price_per_day

        # check if the car is available
        if not car.is_available(start_date, end_date):
            flash('car is not available for the selected dates.')
            return redirect(url_for('car_book', car_id=car_id))

        # create a new booking
        booking = Booking(
            user_id=session['user_id'],
            car_id=car.id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )

        db.session.add(booking)
        db.session.commit()

        # Set car availability to false
        car.availability = False
        db.session.commit()

        flash('Car booked successfully!')
        return redirect(url_for('index'))
    return render_template('car_book.html', car=car)


@app.route('/car_rent/<int:car_id>', methods=['GET', 'POST'])
def car_rent(car_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    car = Car.query.get_or_404(car_id)
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        total_days = (end_date - start_date).days
        total_cost = total_days * car.price_per_day

        new_rental = Rental(
            car_id=car.id,
            user_id=user.id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )

        db.session.add(new_rental)
        db.session.commit()

        return redirect(url_for('customer_home'))

    return render_template('car_rent.html', car=car)


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
