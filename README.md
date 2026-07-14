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
├── app.py              # All Flask routes
├── models.py           # Database models (User, Trek, Booking)
├── templates/          # Jinja2 HTML templates
└── instance/
    └── database.db     # SQLite database (auto-created on first run)
```

## Resetting the Database

To start fresh (clear all data), delete the database file and restart the app:
```
rm instance/database.db
python app.py
```
