from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import get_db, sanitize, validate_csrf
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id') or not session.get('is_admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def csrf_check():
    if not validate_csrf(request.form.get('_csrf','')):
        flash('Security check failed.', 'error')
        return False
    return True

@admin_bp.route('/')
@admin_required
def dashboard():
    db = get_db()
    courses = db.execute("SELECT * FROM courses ORDER BY created_at DESC").fetchall()
    users = db.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    announcements = db.execute("SELECT * FROM announcements ORDER BY created_at DESC").fetchall()
    stats = {
        'courses': db.execute("SELECT COUNT(*) FROM courses").fetchone()[0],
        'users': db.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        'enrollments': db.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0],
        'reviews': db.execute("SELECT COUNT(*) FROM reviews").fetchone()[0],
        'certificates': db.execute("SELECT COUNT(*) FROM certificates").fetchone()[0],
        'beginner': db.execute("SELECT COUNT(*) FROM courses WHERE level='Beginner'").fetchone()[0],
        'intermediate': db.execute("SELECT COUNT(*) FROM courses WHERE level='Intermediate'").fetchone()[0],
        'advanced': db.execute("SELECT COUNT(*) FROM courses WHERE level='Advanced'").fetchone()[0],
    }
    popular = db.execute("""
        SELECT c.title, c.id, COUNT(DISTINCT e.id) as enroll_count, AVG(r.rating) as avg_rating
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id=c.id
        LEFT JOIN reviews r ON r.course_id=c.id
        GROUP BY c.id ORDER BY enroll_count DESC LIMIT 5
    """).fetchall()
    return render_template('admin/dashboard.html', courses=courses, users=users,
                           stats=stats, popular=popular, announcements=announcements)

@admin_bp.route('/courses/new', methods=['GET','POST'])
@admin_required
def new_course():
    if request.method == 'POST':
        if not csrf_check(): return redirect(url_for('admin.new_course'))
        f = request.form
        title = sanitize(f.get('title','').strip())
        if not title:
            flash('Title required.', 'error')
            return render_template('admin/course_form.html', course=None, action='Create')
        db = get_db()
        syllabus = sanitize(f.get('syllabus',''))
        cur = db.execute(
            "INSERT INTO courses (title,description,instructor,instructor_bio,category,level,duration,video_url,tags,syllabus) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (title, sanitize(f.get('description','')), sanitize(f.get('instructor','Staff')),
             sanitize(f.get('instructor_bio','')), sanitize(f.get('category','General')),
             f.get('level','Beginner'), sanitize(f.get('duration','4 weeks')),
             f.get('video_url',''), sanitize(f.get('tags','')), syllabus)
        )
        cid = cur.lastrowid
        for i, line in enumerate([l.strip() for l in syllabus.split('\n') if l.strip()]):
            db.execute("INSERT INTO lessons (course_id,title,position) VALUES (?,?,?)", (cid, line, i))
        db.commit()
        flash(f'Course "{title}" created.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/course_form.html', course=None, action='Create')

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET','POST'])
@admin_required
def edit_course(course_id):
    db = get_db()
    course = db.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course:
        flash('Not found.', 'error'); return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        if not csrf_check(): return redirect(url_for('admin.edit_course', course_id=course_id))
        f = request.form
        title = sanitize(f.get('title','').strip())
        if not title:
            flash('Title required.', 'error')
            return render_template('admin/course_form.html', course=course, action='Update')
        syllabus = sanitize(f.get('syllabus',''))
        db.execute(
            "UPDATE courses SET title=?,description=?,instructor=?,instructor_bio=?,category=?,level=?,duration=?,video_url=?,tags=?,syllabus=? WHERE id=?",
            (title, sanitize(f.get('description','')), sanitize(f.get('instructor','Staff')),
             sanitize(f.get('instructor_bio','')), sanitize(f.get('category','General')),
             f.get('level','Beginner'), sanitize(f.get('duration','4 weeks')),
             f.get('video_url',''), sanitize(f.get('tags','')), syllabus, course_id)
        )
        db.execute("DELETE FROM lessons WHERE course_id=?", (course_id,))
        for i, line in enumerate([l.strip() for l in syllabus.split('\n') if l.strip()]):
            db.execute("INSERT INTO lessons (course_id,title,position) VALUES (?,?,?)", (course_id, line, i))
        db.commit()
        flash(f'Course "{title}" updated.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/course_form.html', course=course, action='Update')

@admin_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    if not csrf_check(): return redirect(url_for('admin.dashboard'))
    db = get_db()
    course = db.execute("SELECT title FROM courses WHERE id=?", (course_id,)).fetchone()
    if course:
        db.execute("DELETE FROM progress WHERE lesson_id IN (SELECT id FROM lessons WHERE course_id=?)", (course_id,))
        db.execute("DELETE FROM lessons WHERE course_id=?", (course_id,))
        db.execute("DELETE FROM reviews WHERE course_id=?", (course_id,))
        db.execute("DELETE FROM certificates WHERE course_id=?", (course_id,))
        db.execute("DELETE FROM enrollments WHERE course_id=?", (course_id,))
        db.execute("DELETE FROM courses WHERE id=?", (course_id,))
        db.commit()
        flash(f'Course "{course["title"]}" deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    if not csrf_check(): return redirect(url_for('admin.dashboard'))
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if user and user['id'] != session['user_id']:
        new_val = 0 if user['is_admin'] else 1
        db.execute("UPDATE users SET is_admin=? WHERE id=?", (new_val, user_id))
        db.commit()
        flash(f'{"Granted" if new_val else "Revoked"} admin for {user["username"]}.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if not csrf_check(): return redirect(url_for('admin.dashboard'))
    if user_id == session['user_id']:
        flash("Cannot delete your own account.", 'error')
        return redirect(url_for('admin.dashboard'))
    db = get_db()
    db.execute("DELETE FROM progress WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM reviews WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM certificates WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM enrollments WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM users WHERE id=?", (user_id,))
    db.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/announcements/new', methods=['POST'])
@admin_required
def new_announcement():
    if not csrf_check(): return redirect(url_for('admin.dashboard'))
    title = sanitize(request.form.get('title','').strip())[:120]
    body  = sanitize(request.form.get('body','').strip())[:1000]
    kind  = request.form.get('kind','info')
    if kind not in ('info','success','warning','danger'):
        kind = 'info'
    if title and body:
        db = get_db()
        db.execute("INSERT INTO announcements (title,body,kind,created_by) VALUES (?,?,?,?)",
                   (title, body, kind, session['user_id']))
        db.commit()
        flash('Announcement posted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/announcements/<int:ann_id>/delete', methods=['POST'])
@admin_required
def delete_announcement(ann_id):
    if not csrf_check(): return redirect(url_for('admin.dashboard'))
    db = get_db()
    db.execute("DELETE FROM announcements WHERE id=?", (ann_id,))
    db.commit()
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
