from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app import get_db, validate_csrf, sanitize
from app.course_content import COURSE_CONTENT
import secrets

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/')
def course_list():
    db = get_db()
    level = request.args.get('level','')
    category = request.args.get('category','')
    tag = request.args.get('tag','')
    q = "SELECT * FROM courses WHERE 1=1"
    params = []
    if level:
        q += " AND level=?"; params.append(level)
    if category:
        q += " AND category=?"; params.append(category)
    if tag:
        q += " AND tags LIKE ?"; params.append(f'%{tag}%')
    q += " ORDER BY created_at DESC"
    courses = db.execute(q, params).fetchall()
    categories = [r[0] for r in db.execute("SELECT DISTINCT category FROM courses ORDER BY category").fetchall()]
    result = []
    for c in courses:
        avg = db.execute("SELECT AVG(rating) FROM reviews WHERE course_id=?", (c['id'],)).fetchone()[0]
        cnt = db.execute("SELECT COUNT(*) FROM reviews WHERE course_id=?", (c['id'],)).fetchone()[0]
        result.append({'course': c, 'avg_rating': round(avg,1) if avg else None, 'review_count': cnt})
    return render_template('course_list.html', courses=result, categories=categories,
                           selected_level=level, selected_category=category, selected_tag=tag)

@courses_bp.route('/<int:course_id>')
def course_detail(course_id):
    db = get_db()
    course = db.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course:
        return "Course not found", 404
    lessons = db.execute("SELECT * FROM lessons WHERE course_id=? ORDER BY position", (course_id,)).fetchall()
    related = db.execute("SELECT * FROM courses WHERE level=? AND id!=? LIMIT 3", (course['level'], course_id)).fetchall()
    reviews = db.execute("""
        SELECT r.*, u.username, u.avatar_color FROM reviews r
        JOIN users u ON u.id=r.user_id WHERE r.course_id=? ORDER BY r.created_at DESC
    """, (course_id,)).fetchall()
    avg_rating = db.execute("SELECT AVG(rating) FROM reviews WHERE course_id=?", (course_id,)).fetchone()[0]
    enrolled = False; completed_lessons = set(); user_review = None; certificate = None
    if session.get('user_id'):
        uid = session['user_id']
        enrolled = db.execute("SELECT id FROM enrollments WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone() is not None
        rows = db.execute("SELECT lesson_id FROM progress WHERE user_id=?", (uid,)).fetchall()
        completed_lessons = {r['lesson_id'] for r in rows}
        user_review = db.execute("SELECT * FROM reviews WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone()
        certificate = db.execute("SELECT * FROM certificates WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone()
        # Auto-issue certificate if all lessons done and enrolled
        if enrolled and lessons and len(completed_lessons.intersection({l['id'] for l in lessons})) == len(lessons) and not certificate:
            code = secrets.token_urlsafe(16)
            db.execute("INSERT OR IGNORE INTO certificates (user_id,course_id,cert_code) VALUES (?,?,?)", (uid, course_id, code))
            db.commit()
            certificate = db.execute("SELECT * FROM certificates WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone()
    tags = [t.strip() for t in (course['tags'] or '').split(',') if t.strip()]
    syllabus = [s.strip() for s in (course['syllabus'] or '').split('\n') if s.strip()]
    rich = COURSE_CONTENT.get(course['title'], {})
    return render_template('course_detail.html', course=course, lessons=lessons, related=related,
                           reviews=reviews, avg_rating=round(avg_rating,1) if avg_rating else None,
                           enrolled=enrolled, completed_lessons=completed_lessons,
                           user_review=user_review, tags=tags, syllabus=syllabus, certificate=certificate,
                           what_you_learn=rich.get('what_you_learn', []),
                           requirements=rich.get('requirements', []),
                           overview=rich.get('overview', ''))

@courses_bp.route('/<int:course_id>/enroll', methods=['POST'])
def enroll(course_id):
    if not session.get('user_id'):
        flash('Please log in to enroll.', 'error')
        return redirect(url_for('auth.login'))
    if not validate_csrf(request.form.get('_csrf','')):
        flash('Security check failed.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    db = get_db()
    try:
        db.execute("INSERT INTO enrollments (user_id,course_id) VALUES (?,?)", (session['user_id'], course_id))
        db.commit()
        flash('Successfully enrolled!', 'success')
    except Exception:
        flash('Already enrolled.', 'info')
    return redirect(url_for('courses.course_detail', course_id=course_id))

@courses_bp.route('/<int:course_id>/progress', methods=['POST'])
def toggle_progress(course_id):
    if not session.get('user_id'):
        return jsonify({'error': 'not logged in'}), 401
    data = request.json or {}
    lesson_id = data.get('lesson_id')
    csrf = data.get('_csrf','')
    if not validate_csrf(csrf):
        return jsonify({'error': 'invalid csrf'}), 403
    if not lesson_id:
        return jsonify({'error': 'missing lesson_id'}), 400
    uid = session['user_id']
    db = get_db()
    # Verify lesson belongs to this course
    lesson = db.execute("SELECT id FROM lessons WHERE id=? AND course_id=?", (lesson_id, course_id)).fetchone()
    if not lesson:
        return jsonify({'error': 'invalid lesson'}), 400
    existing = db.execute("SELECT id FROM progress WHERE user_id=? AND lesson_id=?", (uid, lesson_id)).fetchone()
    if existing:
        db.execute("DELETE FROM progress WHERE user_id=? AND lesson_id=?", (uid, lesson_id))
        done = False
    else:
        db.execute("INSERT INTO progress (user_id,lesson_id) VALUES (?,?)", (uid, lesson_id))
        done = True
    db.commit()
    total = db.execute("SELECT COUNT(*) FROM lessons WHERE course_id=?", (course_id,)).fetchone()[0]
    completed = db.execute("""
        SELECT COUNT(*) FROM progress p JOIN lessons l ON l.id=p.lesson_id
        WHERE p.user_id=? AND l.course_id=?
    """, (uid, course_id)).fetchone()[0]
    cert_code = None
    if done and completed == total and total > 0:
        code = secrets.token_urlsafe(16)
        db.execute("INSERT OR IGNORE INTO certificates (user_id,course_id,cert_code) VALUES (?,?,?)", (uid, course_id, code))
        db.commit()
        cert = db.execute("SELECT cert_code FROM certificates WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone()
        if cert:
            cert_code = cert['cert_code']
    return jsonify({'done': done, 'completed': completed, 'total': total, 'cert_code': cert_code})

@courses_bp.route('/<int:course_id>/review', methods=['POST'])
def submit_review(course_id):
    if not session.get('user_id'):
        flash('Please log in to leave a review.', 'error')
        return redirect(url_for('auth.login'))
    if not validate_csrf(request.form.get('_csrf','')):
        flash('Security check failed.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    uid = session['user_id']
    try:
        rating = int(request.form.get('rating', 5))
    except (ValueError, TypeError):
        rating = 5
    rating = max(1, min(5, rating))
    body = sanitize(request.form.get('body','').strip())[:1000]
    db = get_db()
    if not db.execute("SELECT id FROM enrollments WHERE user_id=? AND course_id=?", (uid, course_id)).fetchone():
        flash('You must be enrolled to leave a review.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    try:
        db.execute("INSERT INTO reviews (user_id,course_id,rating,body) VALUES (?,?,?,?)", (uid, course_id, rating, body))
    except Exception:
        db.execute("UPDATE reviews SET rating=?,body=? WHERE user_id=? AND course_id=?", (rating, body, uid, course_id))
    db.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('courses.course_detail', course_id=course_id))

@courses_bp.route('/certificate/<cert_code>')
def verify_certificate(cert_code):
    db = get_db()
    cert = db.execute("""
        SELECT c.*, u.username, co.title as course_title, co.instructor
        FROM certificates c
        JOIN users u ON u.id=c.user_id
        JOIN courses co ON co.id=c.course_id
        WHERE c.cert_code=?
    """, (cert_code,)).fetchone()
    return render_template('certificate.html', cert=cert, valid=cert is not None)

@courses_bp.route('/<int:course_id>/unenroll', methods=['POST'])
def unenroll(course_id):
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    if not validate_csrf(request.form.get('_csrf','')):
        flash('Security check failed.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    uid = session['user_id']
    db = get_db()
    db.execute("DELETE FROM enrollments WHERE user_id=? AND course_id=?", (uid, course_id))
    # Keep progress and certificate — intentional
    db.commit()
    flash('You have unenrolled. Your progress has been saved.', 'info')
    return redirect(url_for('courses.course_detail', course_id=course_id))

@courses_bp.route('/instructor/<path:name>')
def instructor(name):
    db = get_db()
    courses = db.execute(
        "SELECT * FROM courses WHERE instructor=? ORDER BY level, title", (name,)
    ).fetchall()
    if not courses:
        return "Instructor not found", 404
    result = []
    for c in courses:
        avg = db.execute("SELECT AVG(rating) FROM reviews WHERE course_id=?", (c['id'],)).fetchone()[0]
        cnt = db.execute("SELECT COUNT(*) FROM reviews WHERE course_id=?", (c['id'],)).fetchone()[0]
        result.append({'course': c, 'avg_rating': round(avg,1) if avg else None, 'review_count': cnt})
    return render_template('instructor.html', name=name,
                           bio=courses[0]['instructor_bio'],
                           courses=result)
