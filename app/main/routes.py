from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import get_db, sanitize, validate_csrf

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    db = get_db()
    featured = db.execute("SELECT * FROM courses ORDER BY RANDOM() LIMIT 3").fetchall()
    total = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_enrollments = db.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
    return render_template('home.html', featured=featured, total_courses=total,
                           total_users=total_users, total_enrollments=total_enrollments)

@main_bp.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('auth.login') + '?next=/dashboard')
    db = get_db()
    uid = session['user_id']
    user = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    enrollments = db.execute("""
        SELECT c.*, e.enrolled_at FROM courses c
        JOIN enrollments e ON e.course_id=c.id
        WHERE e.user_id=? ORDER BY e.enrolled_at DESC
    """, (uid,)).fetchall()
    progress_map = {}
    for c in enrollments:
        total = db.execute("SELECT COUNT(*) FROM lessons WHERE course_id=?", (c['id'],)).fetchone()[0]
        done = db.execute("""
            SELECT COUNT(*) FROM progress p JOIN lessons l ON l.id=p.lesson_id
            WHERE p.user_id=? AND l.course_id=?
        """, (uid, c['id'])).fetchone()[0]
        progress_map[c['id']] = {'done': done, 'total': total, 'pct': int(done/total*100) if total else 0}
    certificates = db.execute("SELECT * FROM certificates WHERE user_id=?", (uid,)).fetchall()
    cert_set = {c['course_id'] for c in certificates}
    total_courses = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    return render_template('dashboard.html', user=user, enrollments=enrollments,
                           progress_map=progress_map, total_courses=total_courses,
                           certificates=certificates, cert_set=cert_set)

@main_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    db = get_db()
    uid = session['user_id']
    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf','')):
            flash('Security check failed.', 'error')
        else:
            bio = sanitize(request.form.get('bio','').strip())[:300]
            color = request.form.get('avatar_color','#6366f1')
            allowed_colors = ['#18181b','#6366f1','#ec4899','#f59e0b','#10b981','#3b82f6','#ef4444','#8b5cf6']
            if color not in allowed_colors:
                color = '#18181b'
            db.execute("UPDATE users SET bio=?,avatar_color=? WHERE id=?", (bio, color, uid))
            db.commit()
            flash('Profile updated.', 'success')
    user = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    reviews = db.execute("""
        SELECT r.*, c.title as course_title FROM reviews r
        JOIN courses c ON c.id=r.course_id WHERE r.user_id=? ORDER BY r.created_at DESC
    """, (uid,)).fetchall()
    certs = db.execute("""
        SELECT cert.*, c.title as course_title FROM certificates cert
        JOIN courses c ON c.id=cert.course_id WHERE cert.user_id=? ORDER BY cert.issued_at DESC
    """, (uid,)).fetchall()
    return render_template('profile.html', user=user, reviews=reviews, certificates=certs)

@main_bp.route('/search')
def search():
    query = sanitize(request.args.get('q','').strip())[:100]
    results = []
    if query:
        db = get_db()
        like = f'%{query}%'
        rows = db.execute(
            "SELECT * FROM courses WHERE title LIKE ? OR description LIKE ? OR category LIKE ? OR instructor LIKE ? OR tags LIKE ?",
            (like,like,like,like,like)
        ).fetchall()
        for c in rows:
            avg = db.execute("SELECT AVG(rating) FROM reviews WHERE course_id=?", (c['id'],)).fetchone()[0]
            results.append({'course': c, 'avg_rating': round(avg,1) if avg else None})
    return render_template('search.html', results=results, query=query)

@main_bp.route('/faq')
def faq():
    return render_template('faq.html')

@main_bp.route('/announcements')
def announcements():
    db = get_db()
    items = db.execute("SELECT * FROM announcements ORDER BY created_at DESC").fetchall()
    return render_template('announcements.html', items=items)
