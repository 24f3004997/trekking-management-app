from flask import render_template, redirect, url_for, request, session, flash
from app import app
from models import db, User, Trek, Booking


@app.route('/user/dashboard')
def user_dashboard():
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    available_treks = Trek.query.filter_by(status='Open').all()
    my_bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template('user_dashboard.html', available_treks=available_treks, my_bookings=my_bookings)


@app.route('/user/treks', methods=['GET', 'POST'])
def user_browse_treks():
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    query = Trek.query.filter_by(status='Open')
    difficulty = request.args.get('difficulty')
    location = request.args.get('location')
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if location:
        query = query.filter_by(location=location)
    treks = query.all()
    all_locations = db.session.query(Trek.location).distinct().all()
    return render_template('user_browse_treks.html', treks=treks, all_locations=all_locations)


@app.route('/user/trek/<int:trek_id>')
def user_trek_details(trek_id):
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    return render_template('user_trek_details.html', trek=trek)


@app.route('/user/trek/<int:trek_id>/book')
def user_book_trek(trek_id):
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    if trek.status != 'Open':
        flash('This trek is not open for booking right now')
        return redirect(url_for('user_trek_details', trek_id=trek.id))
    if trek.available_slots <= 0:
        flash('No slots available for this trek')
        return redirect(url_for('user_trek_details', trek_id=trek.id))
    existing = Booking.query.filter_by(user_id=session['user_id'], trek_id=trek.id, status='Booked').first()
    if existing:
        flash('You have already booked this trek')
        return redirect(url_for('user_trek_details', trek_id=trek.id))
    new_booking = Booking(user_id=session['user_id'], trek_id=trek.id, status='Booked')
    trek.available_slots -= 1
    db.session.add(new_booking)
    db.session.commit()
    flash('Trek booked successfully')
    return redirect(url_for('user_my_bookings'))


@app.route('/user/bookings')
def user_my_bookings():
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.booking_date.desc()).all()
    return render_template('user_my_bookings.html', bookings=bookings)


@app.route('/user/bookings/cancel/<int:booking_id>')
def user_cancel_booking(booking_id):
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != session['user_id']:
        flash('This booking does not belong to you')
        return redirect(url_for('user_my_bookings'))
    if booking.status == 'Booked':
        booking.status = 'Cancelled'
        booking.trek.available_slots += 1
        db.session.commit()
        flash('Booking cancelled successfully')
    return redirect(url_for('user_my_bookings'))


@app.route('/user/history')
def user_history():
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    history = Booking.query.filter_by(user_id=session['user_id'], status='Completed').all()
    return render_template('user_history.html', history=history)


@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    if session.get('role') != 'trekker':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.name = request.form['name']
        user.contact = request.form['contact']
        db.session.commit()
        session['name'] = user.name
        flash('Profile updated successfully')
        return redirect(url_for('user_profile'))
    return render_template('user_profile.html', user=user)

@app.route('/api/treks')
def api_treks():
    treks = Trek.query.filter_by(status='Open').all()
    result = []
    for t in treks:
        result.append({
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'difficulty': t.difficulty,
            'duration_days': t.duration_days,
            'available_slots': t.available_slots,
            'status': t.status
        })
    return {'treks': result}