@app.route('/rent_car/<int:car_id>', methods=['GET', 'POST'])
def rent_car(car_id):
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

    return render_template('rent_car.html', car=car)