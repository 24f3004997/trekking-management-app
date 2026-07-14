from flask import render_template, redirect, url_for, request, session, flash
from app import app
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        if user.is_blacklisted:
            flash('You have been blacklisted. Please contact admin')
            return redirect(url_for('login'))
        if user.role == 'staff' and not user.is_approved:
            flash('Your account is pending admin approval')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['name'] = user.name
        session['role'] = user.role

        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        contact = request.form['contact']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        already = User.query.filter_by(email=email).first()
        if already:
            flash('This email is already registered')
            return redirect(url_for('register'))

        new_user = User(
            name=name, email=email,
            password=generate_password_hash(password),
            role=role,
            contact=contact,
            is_approved=(role == 'trekker')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now login')
        return redirect(url_for('login'))

    return render_template('register.html')