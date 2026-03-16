# LearnSphere — Course Learning Portal

A full-featured Flask course learning portal with professional UI.

## Requirements
- Python 3.10+
- Flask only (no other dependencies!)

## Setup

```bash
pip install flask
python run.py
```

Then open http://localhost:5000

## Default Admin Account
- Email: admin@learnsphere.com
- Password: admin123

## Features
- Browse & search courses
- Register / login / logout
- Enroll in courses
- Personal dashboard
- Admin panel (create, edit, delete courses)
- JSON API at /api/courses and /api/stats

## Project Structure
```
app/
  __init__.py          — App factory (Flask + sqlite3, no ORM needed)
  auth/routes.py       — Login, register, logout
  main/routes.py       — Home, dashboard, search
  courses/routes.py    — Course list, detail, enroll
  admin/routes.py      — Admin CRUD (requires admin account)
  api/routes.py        — JSON API endpoints
  templates/           — Jinja2 templates (DM Serif Display + DM Sans)
  static/              — CSS/JS assets
instance/
  learnsphere.db       — SQLite database (auto-created on first run)
run.py                 — Entry point
```

## Architecture Notes
- Zero external dependencies beyond Flask
- Uses Python's built-in `sqlite3` and `hashlib`
- Session-based auth (no flask-login)
- Database auto-initialised with 6 sample courses on first run
