from flask import render_template, redirect, url_for, request, session, flash
from datetime import datetime
from app import app
from models import db, User, Trek, Booking


@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    return render_template('admin_dashboard.html', total_treks=total_treks, total_users=total_users,
                            total_staff=total_staff, total_bookings=total_bookings, recent_bookings=recent_bookings)


@app.route('/admin/treks')
def admin_treks():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    all_treks = Trek.query.all()
    return render_template('admin_treks.html', treks=all_treks)


@app.route('/admin/treks/add', methods=['GET', 'POST'])
def admin_add_trek():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    staff_list = User.query.filter_by(role='staff', is_approved=True).all()
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        available_slots = int(request.form['available_slots'])

        if end_date < start_date:
            flash('End date cannot be before start date')
            return redirect(url_for('admin_add_trek'))

        if available_slots < 0:
            flash('Available slots cannot be negative')
            return redirect(url_for('admin_add_trek'))

        new_trek = Trek(
            name=request.form['name'], location=request.form['location'],
            difficulty=request.form['difficulty'],
            duration_days=int(request.form['duration_days']),
            available_slots=available_slots,
            assigned_staff_id=int(request.form['assigned_staff_id']) if request.form['assigned_staff_id'] else None,
            status=request.form['status'], description=request.form['description'],
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_trek)
        db.session.commit()
        flash('New trek added successfully')
        return redirect(url_for('admin_treks'))
    return render_template('admin_add_trek.html', staff_list=staff_list, trek=None)


@app.route('/admin/treks/edit/<int:trek_id>', methods=['GET', 'POST'])
def admin_edit_trek(trek_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    staff_list = User.query.filter_by(role='staff', is_approved=True).all()
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        available_slots = int(request.form['available_slots'])

        if end_date < start_date:
            flash('End date cannot be before start date')
            return redirect(url_for('admin_edit_trek', trek_id=trek.id))

        if available_slots < 0:
            flash('Available slots cannot be negative')
            return redirect(url_for('admin_edit_trek', trek_id=trek.id))

        trek.name = request.form['name']
        trek.location = request.form['location']
        trek.difficulty = request.form['difficulty']
        trek.duration_days = int(request.form['duration_days'])
        trek.available_slots = available_slots
        assigned_staff_id = request.form['assigned_staff_id']
        trek.assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None
        trek.status = request.form['status']
        trek.description = request.form['description']
        trek.start_date = start_date
        trek.end_date = end_date
        db.session.commit()
        flash('Trek updated successfully')
        return redirect(url_for('admin_treks'))
    return render_template('admin_add_trek.html', staff_list=staff_list, trek=trek)

@app.route('/admin/treks/delete/<int:trek_id>')
def admin_delete_trek(trek_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted successfully')
    return redirect(url_for('admin_treks'))


@app.route('/admin/staff')
def admin_staff():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    pending_staff = User.query.filter_by(role='staff', is_approved=False, is_blacklisted=False).all()
    approved_staff = User.query.filter_by(role='staff', is_approved=True, is_blacklisted=False).all()
    blacklisted_staff = User.query.filter_by(role='staff', is_blacklisted=True).all()
    return render_template('admin_staff.html', pending_staff=pending_staff,
                            approved_staff=approved_staff, blacklisted_staff=blacklisted_staff)


@app.route('/admin/staff/approve/<int:staff_id>')
def admin_approve_staff(staff_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    staff = User.query.get_or_404(staff_id)
    staff.is_approved = True
    db.session.commit()
    flash('Staff approved successfully')
    return redirect(url_for('admin_staff'))


@app.route('/admin/staff/reject/<int:staff_id>')
def admin_reject_staff(staff_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    staff = User.query.get_or_404(staff_id)
    staff.is_blacklisted = True
    db.session.commit()
    flash('Staff rejected and blacklisted')
    return redirect(url_for('admin_staff'))


@app.route('/admin/staff/blacklist/<int:staff_id>')
def admin_blacklist_staff(staff_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    staff = User.query.get_or_404(staff_id)
    staff.is_blacklisted = True
    db.session.commit()
    flash('Staff blacklisted successfully')
    return redirect(url_for('admin_staff'))


@app.route('/admin/users')
def admin_users():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    all_users = User.query.filter_by(role='trekker').all()
    return render_template('admin_users.html', users=all_users)


@app.route('/admin/users/blacklist/<int:user_id>')
def admin_blacklist_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = True
    db.session.commit()
    flash('User blacklisted successfully')
    return redirect(url_for('admin_users'))


@app.route('/admin/users/unblacklist/<int:user_id>')
def admin_unblacklist_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = False
    db.session.commit()
    flash('User unblacklisted successfully')
    return redirect(url_for('admin_users'))


@app.route('/admin/bookings')
def admin_bookings():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    all_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin_bookings.html', bookings=all_bookings)


@app.route('/admin/search', methods=['GET', 'POST'])
def admin_search():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    trek_results = []
    staff_results = []
    user_results = []
    query = ''

    if request.method == 'POST':
        query = request.form['query']

        if query.isdigit():
            trek_results = Trek.query.filter(
                (Trek.name.contains(query)) | (Trek.id == int(query))
            ).all()
            staff_results = User.query.filter(
                User.role == 'staff'
            ).filter(
                (User.name.contains(query)) | (User.id == int(query))
            ).all()
            user_results = User.query.filter(
                User.role == 'trekker'
            ).filter(
                (User.name.contains(query)) | (User.id == int(query))
            ).all()
        else:
            trek_results = Trek.query.filter(Trek.name.contains(query)).all()
            staff_results = User.query.filter(User.role == 'staff', User.name.contains(query)).all()
            user_results = User.query.filter(User.role == 'trekker', User.name.contains(query)).all()

    return render_template('admin_search.html', trek_results=trek_results,
                            staff_results=staff_results, user_results=user_results, query=query)