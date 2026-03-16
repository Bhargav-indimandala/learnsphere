from flask import Blueprint, jsonify, request
from app import get_db

api_bp = Blueprint('api', __name__)

@api_bp.route('/courses')
def courses():
    db = get_db()
    level = request.args.get('level')
    category = request.args.get('category')
    query = "SELECT * FROM courses WHERE 1=1"
    params = []
    if level:
        query += " AND level=?"
        params.append(level)
    if category:
        query += " AND category=?"
        params.append(category)
    query += " ORDER BY title"
    rows = db.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

@api_bp.route('/courses/<int:course_id>')
def course(course_id):
    db = get_db()
    row = db.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not row:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(dict(row))

@api_bp.route('/stats')
def stats():
    db = get_db()
    return jsonify({
        'total_courses': db.execute("SELECT COUNT(*) FROM courses").fetchone()[0],
        'total_users': db.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        'total_enrollments': db.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0],
        'levels': {
            'Beginner': db.execute("SELECT COUNT(*) FROM courses WHERE level='Beginner'").fetchone()[0],
            'Intermediate': db.execute("SELECT COUNT(*) FROM courses WHERE level='Intermediate'").fetchone()[0],
            'Advanced': db.execute("SELECT COUNT(*) FROM courses WHERE level='Advanced'").fetchone()[0],
        }
    })
