import re
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import (get_db, hash_password, verify_password, upgrade_password_if_needed,
                 rate_limit, sanitize, validate_csrf, generate_otp, verify_otp)

auth_bp = Blueprint('auth', __name__)
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

# ── Register ─────────────────────────────────────────────────────────────────

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed. Please try again.', 'error')
            return render_template('auth/register.html')

        ip = request.remote_addr or 'unknown'
        if not rate_limit(f'register:{ip}', limit=3, window=600):
            flash('Too many registration attempts. Please wait and try again.', 'error')
            return render_template('auth/register.html')

        username = sanitize(request.form.get('username', '').strip())
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        errors = []
        if not all([username, email, password, confirm]):
            errors.append('All fields are required.')
        if username and (len(username) < 3 or len(username) > 32):
            errors.append('Username must be 3–32 characters.')
        if username and not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append('Username can only contain letters, numbers, _ and -.')
        if email and not EMAIL_RE.match(email):
            errors.append('Invalid email address.')
        if password and len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors: flash(e, 'error')
            return render_template('auth/register.html')

        db = get_db()
        if db.execute("SELECT id FROM users WHERE email=? OR username=?", (email, username)).fetchone():
            flash('Email or username already in use.', 'error')
            return render_template('auth/register.html')

        # Store pending registration in session, send OTP
        session['_pending_reg'] = {'username': username, 'email': email, 'password': hash_password(password)}
        generate_otp(db, email, 'verify_email')
        flash(f'A 6-digit verification code has been sent to {email} (check your terminal).', 'info')
        return redirect(url_for('auth.verify_email'))

    return render_template('auth/register.html')


@auth_bp.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    pending = session.get('_pending_reg')
    if not pending:
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/otp.html', purpose='verify_email',
                                   email=pending['email'], action_url=url_for('auth.verify_email'))

        ip = request.remote_addr or 'unknown'
        if not rate_limit(f'otp:{ip}', limit=10, window=300):
            flash('Too many attempts. Please wait a moment.', 'error')
            return render_template('auth/otp.html', purpose='verify_email',
                                   email=pending['email'], action_url=url_for('auth.verify_email'))

        code = request.form.get('otp', '').strip()
        db   = get_db()

        if verify_otp(db, pending['email'], code, 'verify_email'):
            db.execute("INSERT INTO users (username, email, password_hash) VALUES (?,?,?)",
                       (pending['username'], pending['email'], pending['password']))
            db.commit()
            user = db.execute("SELECT * FROM users WHERE email=?", (pending['email'],)).fetchone()
            session.pop('_pending_reg', None)
            session['user_id']      = user['id']
            session['username']     = user['username']
            session['is_admin']     = bool(user['is_admin'])
            session['_last_active'] = time.time()
            session.permanent       = True
            flash('Email verified! Welcome to LearnSphere.', 'success')
            return redirect(url_for('main.dashboard'))

        flash('Invalid or expired code. Please try again.', 'error')

    return render_template('auth/otp.html', purpose='verify_email',
                           email=pending['email'], action_url=url_for('auth.verify_email'))


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    if not validate_csrf(request.form.get('_csrf', '')):
        flash('Security check failed.', 'error')
        return redirect(request.referrer or url_for('main.home'))

    ip = request.remote_addr or 'unknown'
    if not rate_limit(f'resend:{ip}', limit=3, window=300):
        flash('Too many resend attempts. Please wait.', 'error')
        return redirect(request.referrer or url_for('main.home'))

    purpose = request.form.get('purpose', '')
    db = get_db()

    if purpose == 'verify_email':
        pending = session.get('_pending_reg')
        if pending:
            generate_otp(db, pending['email'], 'verify_email')
            flash('A new code has been sent (check terminal).', 'info')
        return redirect(url_for('auth.verify_email'))

    if purpose == '2fa':
        email = session.get('_2fa_email', '')
        if email:
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if user:
                generate_otp(db, email, '2fa', user_id=user['id'])
                flash('A new code has been sent (check terminal).', 'info')
        return redirect(url_for('auth.two_factor'))

    if purpose == 'reset_password':
        email = session.get('_reset_email', '')
        if email:
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if user:
                generate_otp(db, email, 'reset_password', user_id=user['id'])
                flash('A new code has been sent (check terminal).', 'info')
        return redirect(url_for('auth.reset_verify'))

    return redirect(url_for('main.home'))


# ── Login + 2FA ───────────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed. Please try again.', 'error')
            return render_template('auth/login.html')

        ip    = request.remote_addr or 'unknown'
        email = request.form.get('email', '').strip().lower()

        if not rate_limit(f'login:{ip}', limit=5, window=300):
            flash('Too many login attempts. Please wait 5 minutes.', 'error')
            return render_template('auth/login.html')

        password = request.form.get('password', '')
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')

        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if user and verify_password(user['password_hash'], password):
            upgrade_password_if_needed(db, user['id'], user['password_hash'], password)
            # Send 2FA OTP
            generate_otp(db, email, '2fa', user_id=user['id'])
            session['_2fa_email'] = email
            session['_2fa_next']  = request.args.get('next', '')
            flash(f'Password correct! A 6-digit code has been sent to {email} (check terminal).', 'info')
            return redirect(url_for('auth.two_factor'))

        flash('Invalid email or password.', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/two-factor', methods=['GET', 'POST'])
def two_factor():
    email = session.get('_2fa_email')
    if not email:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/otp.html', purpose='2fa',
                                   email=email, action_url=url_for('auth.two_factor'))

        ip = request.remote_addr or 'unknown'
        if not rate_limit(f'otp:{ip}', limit=10, window=300):
            flash('Too many attempts. Please wait.', 'error')
            return render_template('auth/otp.html', purpose='2fa',
                                   email=email, action_url=url_for('auth.two_factor'))

        code = request.form.get('otp', '').strip()
        db   = get_db()

        if verify_otp(db, email, code, '2fa'):
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            next_page = session.pop('_2fa_next', '')
            session.pop('_2fa_email', None)
            session['user_id']      = user['id']
            session['username']     = user['username']
            session['is_admin']     = bool(user['is_admin'])
            session['_last_active'] = time.time()
            session.permanent       = True
            flash(f"Welcome back, {user['username']}!", 'success')
            if next_page and next_page.startswith('/') and not next_page.startswith('//'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))

        flash('Invalid or expired code. Please try again.', 'error')

    return render_template('auth/otp.html', purpose='2fa',
                           email=email, action_url=url_for('auth.two_factor'))


# ── Password reset ────────────────────────────────────────────────────────────

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/forgot_password.html')

        ip    = request.remote_addr or 'unknown'
        email = request.form.get('email', '').strip().lower()

        if not rate_limit(f'forgot:{ip}', limit=3, window=600):
            flash('Too many attempts. Please wait.', 'error')
            return render_template('auth/forgot_password.html')

        if not EMAIL_RE.match(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/forgot_password.html')

        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        # Always show same message to prevent email enumeration
        if user:
            generate_otp(db, email, 'reset_password', user_id=user['id'])
        flash('If that email exists, a reset code has been sent (check terminal).', 'info')
        session['_reset_email'] = email
        return redirect(url_for('auth.reset_verify'))

    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-verify', methods=['GET', 'POST'])
def reset_verify():
    email = session.get('_reset_email')
    if not email:
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/otp.html', purpose='reset_password',
                                   email=email, action_url=url_for('auth.reset_verify'))

        ip = request.remote_addr or 'unknown'
        if not rate_limit(f'otp:{ip}', limit=10, window=300):
            flash('Too many attempts. Please wait.', 'error')
            return render_template('auth/otp.html', purpose='reset_password',
                                   email=email, action_url=url_for('auth.reset_verify'))

        code = request.form.get('otp', '').strip()
        db   = get_db()

        if verify_otp(db, email, code, 'reset_password'):
            session['_reset_verified'] = email
            session.pop('_reset_email', None)
            return redirect(url_for('auth.reset_password'))

        flash('Invalid or expired code. Please try again.', 'error')

    return render_template('auth/otp.html', purpose='reset_password',
                           email=email, action_url=url_for('auth.reset_verify'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = session.get('_reset_verified')
    if not email:
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/reset_password.html')

        new_pw  = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        if len(new_pw) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('auth/reset_password.html')
        if new_pw != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html')

        db = get_db()
        db.execute("UPDATE users SET password_hash=? WHERE email=?",
                   (hash_password(new_pw), email))
        db.commit()
        session.pop('_reset_verified', None)
        flash('Password reset successfully! Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')


# ── Logout + change password ─────────────────────────────────────────────────

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if not validate_csrf(request.form.get('_csrf', '')):
            flash('Security check failed.', 'error')
            return render_template('auth/change_password.html')

        current = request.form.get('current_password', '')
        new_pw  = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()

        if not verify_password(user['password_hash'], current):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        if len(new_pw) < 8:
            flash('New password must be at least 8 characters.', 'error')
            return render_template('auth/change_password.html')
        if new_pw != confirm:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')

        db.execute("UPDATE users SET password_hash=? WHERE id=?",
                   (hash_password(new_pw), session['user_id']))
        db.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('auth/change_password.html')
