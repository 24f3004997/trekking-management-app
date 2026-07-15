# Trekking Management Application

A Flask-based web application for managing trekking activities, with three roles: Admin, Trek Staff, and Trekker (User).

## Tech Stack

- **Backend:** Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Frontend:** Jinja2 templates, HTML, Bootstrap 5 (CDN)

## How to Run

1. Make sure Python 3.8+ is installed.

2. Install the required packages:
   ```
   pip install flask flask_sqlalchemy
   ```

3. Run the application:
   ```
   python run.py
   ```

   **Important:** Always run `run.py`, not `app.py` directly. Routes are split
   into separate files under `routes/` (auth, admin, staff, user), and each of
   them does `from app import app`. Running `app.py` directly would cause
   Python to import it twice under two different module names (`__main__`
   and `app`), creating two separate Flask app instances — one that actually
   runs, and one where the routes got registered. This would make every page
   return a 404. `run.py` avoids this by importing `app.py` only once, as the
   `app` module.

4. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

5. On first run, the database is created automatically (`instance/database.db`) along with a default Admin account:
   - **Email:** admin@trek.com
   - **Password:** admin123

   Trek Staff and Trekkers can register from the Register page. New Trek Staff accounts require Admin approval before they can log in.

## Project Structure

```
trekking_app/
├── app.py              # Flask app setup, database init, admin seeding
├── run.py              # Entry point — run this file to start the server
├── models.py           # Database models (User, Trek, Booking)
├── routes/
│   ├── auth.py         # Login, register, logout
│   ├── admin.py        # Admin routes
│   ├── staff.py        # Trek Staff routes
│   └── user.py         # Trekker routes
├── templates/          # Jinja2 HTML templates
└── instance/
    └── database.db     # SQLite database (auto-created on first run)
```

## Resetting the Database

To start fresh (clear all data), delete the database file and restart the app:
```
rm instance/database.db
python run.py
```