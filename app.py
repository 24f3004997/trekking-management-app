from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'trekking_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()
    existing_admin = User.query.filter_by(role='admin').first()
    if not existing_admin:
        admin_user = User(
            name='Admin',
            email='admin@trek.com',
            password=generate_password_hash('admin123'),
            role='admin',
            is_approved=True
        )
        db.session.add(admin_user)
        db.session.commit()

from routes import auth, admin, staff, user

if __name__ == '__main__':
    app.run(debug=True)