from flask import render_template, redirect, url_for, request, session, flash
from app import app
from models import db, User, Trek, Booking


@app.route('/staff/dashboard')
def staff_dashboard():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    staff_id = session['user_id']
    my_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
    total_participants = 0
    for t in my_treks:
        total_participants += Booking.query.filter_by(trek_id=t.id, status='Booked').count()
    open_treks = Trek.query.filter_by(assigned_staff_id=staff_id, status='Open').count()
    return render_template('staff_dashboard.html', my_treks=my_treks,
                            total_participants=total_participants, open_treks=open_treks)


@app.route('/staff/mytreks')
def staff_my_treks():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))

    staff_id = session['user_id']
    my_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()

    # Redirect if only one trek is assigned
    if len(my_treks) == 1:
        return redirect(url_for('staff_manage_trek', trek_id=my_treks[0].id))

    # Otherwise show the list to choose from
    return render_template('staff_my_treks.html', my_treks=my_treks)


@app.route('/staff/trek/<int:trek_id>', methods=['GET', 'POST'])
def staff_manage_trek(trek_id):
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    if trek.assigned_staff_id != session['user_id']:
        flash('This trek is not assigned to you')
        return redirect(url_for('staff_dashboard'))

    if request.method == 'POST':
        trek.available_slots = int(request.form['available_slots'])
        trek.status = request.form['status']
        db.session.commit()
        flash('Trek updated successfully')
        return redirect(url_for('staff_manage_trek', trek_id=trek.id))

    participants = Booking.query.filter_by(trek_id=trek.id).all()
    return render_template('staff_manage_trek.html', trek=trek, participants=participants)


@app.route('/staff/trek/<int:trek_id>/status/<new_status>')
def staff_update_trek_status(trek_id, new_status):
    if session.get('role') != 'staff':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    if trek.assigned_staff_id != session['user_id']:
        flash('This trek is not assigned to you')
        return redirect(url_for('staff_dashboard'))
    trek.status = new_status
    db.session.commit()
    if new_status == 'Completed':
        bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
        for b in bookings:
            b.status = 'Completed'
        db.session.commit()
    flash('Trek status updated successfully')
    return redirect(url_for('staff_manage_trek', trek_id=trek.id))


@app.route('/staff/participants')
def staff_participants():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))

    staff_id = session['user_id']
    my_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
    my_trek_ids = [t.id for t in my_treks]

    participants = Booking.query.filter(Booking.trek_id.in_(my_trek_ids)).all()

    return render_template('staff_participants.html', participants=participants)


@app.route('/staff/profile', methods=['GET', 'POST'])
def staff_profile():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))

    staff = User.query.get(session['user_id'])

    if request.method == 'POST':
        staff.name = request.form['name']
        staff.contact = request.form['contact']
        db.session.commit()
        session['name'] = staff.name
        flash('Profile updated successfully')
        return redirect(url_for('staff_profile'))

    return render_template('staff_profile.html', staff=staff)