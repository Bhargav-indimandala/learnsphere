import sqlite3
import os
import secrets
import hashlib
import hmac
import time
import html
from flask import Flask, g, session, request, abort, render_template

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'learnsphere.db')

# ── Security helpers ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """PBKDF2-HMAC-SHA256, 260k iterations, hex-encoded."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 260_000)
    return f"pbkdf2$sha256$260000${salt}${dk.hex()}"

def verify_password(stored: str, password: str) -> bool:
    if stored.startswith('pbkdf2$'):
        _, alg, iters, salt, hx = stored.split('$')
        dk = hashlib.pbkdf2_hmac(alg, password.encode(), salt.encode(), int(iters))
        return hmac.compare_digest(dk.hex(), hx)
    # Legacy sha256 fallback (auto-upgrades on next login)
    return hmac.compare_digest(stored, hashlib.sha256(password.encode()).hexdigest())

def upgrade_password_if_needed(db, user_id: int, stored: str, password: str):
    """Upgrade legacy sha256 hash to PBKDF2 on successful login."""
    if not stored.startswith('pbkdf2$'):
        db.execute("UPDATE users SET password_hash=? WHERE id=?",
                   (hash_password(password), user_id))
        db.commit()

def generate_csrf_token() -> str:
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_hex(32)
    return session['_csrf']

def validate_csrf(token: str) -> bool:
    return hmac.compare_digest(session.get('_csrf', ''), token or '')

def sanitize(text: str) -> str:
    """Escape HTML in user-supplied strings."""
    return html.escape(str(text or ''), quote=True)

# ── Rate limiter ─────────────────────────────────────────────────────────────
# Simple in-process store: {key: [timestamp, ...]}
_rl_store: dict = {}
_rl_clean_at: float = 0.0

def rate_limit(key: str, limit: int = 5, window: int = 300) -> bool:
    """Return True if request is allowed, False if blocked."""
    global _rl_clean_at
    now = time.time()
    if now > _rl_clean_at:
        cutoff = now - window
        for k in list(_rl_store):
            _rl_store[k] = [t for t in _rl_store[k] if t > cutoff]
            if not _rl_store[k]:
                del _rl_store[k]
        _rl_clean_at = now + 60
    hits = _rl_store.setdefault(key, [])
    hits[:] = [t for t in hits if t > now - window]
    if len(hits) >= limit:
        return False
    hits.append(now)
    return True


# ── OTP helpers ──────────────────────────────────────────────────────────────

def generate_otp(db, email: str, purpose: str, user_id=None, ttl: int = 600) -> str:
    """
    Generate a 6-digit OTP, store it, and return the code.
    purpose: 'verify_email' | '2fa' | 'reset_password'
    Prints to terminal (swap send_otp_email() for real email in production).
    """
    import time, random
    code = f"{random.SystemRandom().randint(0, 999999):06d}"
    expires = time.time() + ttl
    # Invalidate any existing unused OTPs for same email+purpose
    db.execute(
        "UPDATE otp_tokens SET used=1 WHERE email=? AND purpose=? AND used=0",
        (email, purpose)
    )
    db.execute(
        "INSERT INTO otp_tokens (user_id, email, code, purpose, expires_at) VALUES (?,?,?,?,?)",
        (user_id, email.lower(), code, purpose, expires)
    )
    db.commit()
    _send_otp(email, code, purpose, ttl)
    return code

def verify_otp(db, email: str, code: str, purpose: str) -> bool:
    """Validate OTP — marks as used on success. Returns True if valid."""
    import time
    row = db.execute(
        "SELECT * FROM otp_tokens WHERE email=? AND code=? AND purpose=? AND used=0 ORDER BY id DESC LIMIT 1",
        (email.lower(), code.strip(), purpose)
    ).fetchone()
    if not row:
        return False
    if time.time() > row['expires_at']:
        db.execute("UPDATE otp_tokens SET used=1 WHERE id=?", (row['id'],))
        db.commit()
        return False
    db.execute("UPDATE otp_tokens SET used=1 WHERE id=?", (row['id'],))
    db.commit()
    return True

def _send_otp(email: str, code: str, purpose: str, ttl: int):
    """
    DEV MODE — prints OTP to terminal.
    Replace this function body with your SMTP/SendGrid/etc call in production.
    """
    labels = {
        'verify_email':    'Email Verification',
        '2fa':             'Login Verification (2FA)',
        'reset_password':  'Password Reset',
    }
    label = labels.get(purpose, purpose)
    print("\n" + "="*55)
    print(f"  📬 LearnSphere OTP — {label}")
    print(f"  To:      {email}")
    print(f"  Code:    {code}")
    print(f"  Expires: {ttl // 60} minutes")
    print("="*55 + "\n")

# ── DB helpers ───────────────────────────────────────────────────────────────

def get_db():
    if 'db' not in g:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                bio TEXT DEFAULT '',
                avatar_color TEXT DEFAULT '#6366f1',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                instructor TEXT DEFAULT 'Staff',
                instructor_bio TEXT DEFAULT '',
                category TEXT DEFAULT 'General',
                level TEXT DEFAULT 'Beginner',
                duration TEXT DEFAULT '4 weeks',
                video_url TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                syllabus TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, course_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            );
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                position INTEGER DEFAULT 0,
                FOREIGN KEY(course_id) REFERENCES courses(id)
            );
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lesson_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, lesson_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(lesson_id) REFERENCES lessons(id)
            );
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                body TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, course_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            );
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                kind TEXT DEFAULT 'info',
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(created_by) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS otp_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                email TEXT NOT NULL,
                code TEXT NOT NULL,
                purpose TEXT NOT NULL,
                used INTEGER DEFAULT 0,
                expires_at REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cert_code TEXT UNIQUE NOT NULL,
                UNIQUE(user_id, course_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            );
        """)

        # Migrate columns
        cols = [r[1] for r in db.execute("PRAGMA table_info(courses)").fetchall()]
        for col, defval in [("video_url","''"),("tags","''"),("syllabus","''"),("instructor_bio","''")]:
            if col not in cols:
                db.execute(f"ALTER TABLE courses ADD COLUMN {col} TEXT DEFAULT {defval}")
        ucols = [r[1] for r in db.execute("PRAGMA table_info(users)").fetchall()]
        for col, defval in [("bio","''"),("avatar_color","'#6366f1'")]:
            if col not in ucols:
                db.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT {defval}")

        count = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        if count == 0:
            _seed_data(db)

def _seed_data(db):
    courses = [
        ("Python for Beginners","Learn Python from scratch with hands-on projects covering variables, loops, functions, OOP, and file I/O. Perfect for absolute beginners who want a solid foundation.","Dr. Sarah Chen","Stanford researcher with 10+ years teaching Python","Programming","Beginner","6 weeks","https://www.youtube.com/embed/kqtD5dpn9C8","python,beginner,programming,oop","Week 1: Variables & Data Types\nWeek 2: Control Flow & Loops\nWeek 3: Functions & Scope\nWeek 4: Object-Oriented Programming\nWeek 5: File I/O & Exceptions\nWeek 6: Capstone Project"),
        ("Data Science Fundamentals","Master pandas, numpy, matplotlib and scikit-learn. Build and evaluate real ML models through guided projects and industry case studies.","Prof. James Miller","Former Google data scientist, published author","Data Science","Intermediate","8 weeks","https://www.youtube.com/embed/ua-CiDNNj30","data science,pandas,numpy,machine learning,statistics","Week 1: NumPy Arrays\nWeek 2: Pandas DataFrames\nWeek 3: Data Visualisation\nWeek 4: Statistical Analysis\nWeek 5: Linear Regression\nWeek 6: Classification Models\nWeek 7: Model Evaluation\nWeek 8: Capstone Project"),
        ("Web Development with Flask","Build full-stack web apps with Flask, SQLite, and modern CSS. Deploy to the cloud. Covers authentication, REST APIs, testing, and production best practices.","Emily Rodriguez","Senior engineer at Stripe, open-source contributor","Web Dev","Intermediate","10 weeks","https://www.youtube.com/embed/Z1RJmh_OqeA","flask,web,python,backend,api,sqlite","Week 1-2: Flask Basics & Routing\nWeek 3: Jinja2 Templates & Forms\nWeek 4: SQLite & Database Design\nWeek 5: User Authentication\nWeek 6: REST API Design\nWeek 7: Testing & Debugging\nWeek 8: Frontend Integration\nWeek 9: Cloud Deployment\nWeek 10: Capstone Project"),
        ("Machine Learning A-Z","Deep dive into supervised, unsupervised and reinforcement learning. Covers neural networks, SVMs, clustering, and more with scikit-learn and PyTorch.","Dr. Alex Kim","AI researcher, PhD MIT, 50+ published papers","AI & ML","Advanced","12 weeks","https://www.youtube.com/embed/GwIo3gDZCVQ","machine learning,ai,deep learning,neural networks,pytorch,sklearn","Week 1-2: ML Foundations & Math\nWeek 3-4: Supervised Learning\nWeek 5-6: Unsupervised Learning\nWeek 7-8: Neural Networks\nWeek 9: Convolutional Networks\nWeek 10: Recurrent Networks\nWeek 11: Reinforcement Learning\nWeek 12: Capstone Project"),
        ("JavaScript & React","From DOM manipulation to modern React hooks and state management. Build real SPAs, integrate REST APIs, and learn testing with Jest and React Testing Library.","Tom Walsh","Frontend lead at Shopify, React contributor","Web Dev","Beginner","8 weeks","https://www.youtube.com/embed/w7ejDZ8SWv8","javascript,react,frontend,hooks,spa,jest","Week 1: JS Fundamentals\nWeek 2: DOM & Events\nWeek 3: Async JS & Promises\nWeek 4: React Basics\nWeek 5: Hooks & State Management\nWeek 6: React Router\nWeek 7: API Integration\nWeek 8: Testing & Deployment"),
        ("SQL & Database Design","Relational database fundamentals, advanced query optimisation, indexing, normalisation, and schema design patterns used in production at scale.","Lisa Park","Database architect, 15 years at Oracle and Amazon","Databases","Beginner","5 weeks","https://www.youtube.com/embed/HXV3zeQKqGY","sql,databases,postgresql,schema,indexing,normalisation","Week 1: SQL Basics & SELECT\nWeek 2: Joins & Aggregations\nWeek 3: Schema Design & Normalisation\nWeek 4: Indexing & Query Optimisation\nWeek 5: Transactions & Capstone"),
        ("DevOps & CI/CD","Master Docker, GitHub Actions, Kubernetes basics and cloud deployment pipelines. Build and ship software like a senior engineer from day one.","Marcus Johnson","DevOps engineer at Netflix, CNCF contributor","DevOps","Intermediate","8 weeks","https://www.youtube.com/embed/PzsRELKD6PM","devops,docker,kubernetes,ci/cd,github actions,cloud","Week 1: Linux & Shell Scripting\nWeek 2: Docker Fundamentals\nWeek 3: Docker Compose\nWeek 4: GitHub Actions CI\nWeek 5: CD Pipelines\nWeek 6: Kubernetes Basics\nWeek 7: Cloud Deployment (AWS/GCP)\nWeek 8: Monitoring & Capstone"),
        ("Cybersecurity Fundamentals","Learn ethical hacking, network security, cryptography, and how to defend systems. Hands-on labs using industry-standard tools in a safe sandbox environment.","Dr. Priya Nair","CISSP-certified, former NSA security analyst","Security","Intermediate","9 weeks","https://www.youtube.com/embed/3Kq1MIfTWCE","cybersecurity,hacking,cryptography,networking,penetration testing","Week 1: Security Mindset & Threat Modelling\nWeek 2: Networking & Protocols\nWeek 3: Cryptography\nWeek 4: Web Application Security\nWeek 5: Network Scanning & Enumeration\nWeek 6: Exploitation Basics\nWeek 7: Defence & Hardening\nWeek 8: Incident Response\nWeek 9: Capstone CTF"),
        ("iOS Development with Swift","Build real iPhone apps from scratch using Swift and SwiftUI. Ship your first app to the App Store with guidance from an Apple-certified instructor.","Aisha Patel","iOS engineer at Apple, Swift open-source contributor","Mobile","Intermediate","10 weeks","https://www.youtube.com/embed/comQ1-x2a1Q","swift,ios,swiftui,xcode,mobile,apple","Week 1-2: Swift Language Fundamentals\nWeek 3: SwiftUI Basics\nWeek 4: Navigation & Data Flow\nWeek 5: Networking & APIs\nWeek 6: Local Data & CoreData\nWeek 7: Animations & Gestures\nWeek 8: Push Notifications\nWeek 9: App Store Submission\nWeek 10: Capstone App"),
        ("UI/UX Design Fundamentals","Learn the full design process — research, wireframing, prototyping, and usability testing — using Figma. Build a portfolio-ready case study.","Zara Ahmed","Senior UX designer at Airbnb, design systems lead","Design","Beginner","6 weeks","https://www.youtube.com/embed/c9Wg6Cb_YlU","ux,ui,figma,design,wireframing,prototyping","Week 1: Design Thinking\nWeek 2: User Research\nWeek 3: Wireframing\nWeek 4: Figma & Prototyping\nWeek 5: Usability Testing\nWeek 6: Portfolio Case Study"),
        ("Cloud Computing with AWS","Hands-on AWS: EC2, S3, Lambda, RDS, IAM, and VPC. Pass the AWS Solutions Architect Associate exam with practical labs and mock tests.","Ben Carter","AWS Solutions Architect, 7x AWS certified","Cloud","Advanced","10 weeks","https://www.youtube.com/embed/SOTamWNgDKc","aws,cloud,ec2,s3,lambda,serverless,devops","Week 1: AWS Fundamentals & IAM\nWeek 2: Compute (EC2 & Lambda)\nWeek 3: Storage (S3 & EBS)\nWeek 4: Databases (RDS & DynamoDB)\nWeek 5: Networking (VPC)\nWeek 6: Security & Compliance\nWeek 7: Monitoring & Logging\nWeek 8: Serverless Architecture\nWeek 9: Cost Optimisation\nWeek 10: Mock Exam & Capstone"),
        ("Blockchain & Web3","Understand blockchain fundamentals, write Solidity smart contracts, and build decentralised apps (dApps) on Ethereum using Hardhat and ethers.js.","Kai Nakamura","Ethereum core contributor, DeFi protocol founder","Blockchain","Advanced","8 weeks","https://www.youtube.com/embed/gyMwXuJrbJQ","blockchain,ethereum,solidity,web3,dapps,defi","Week 1: Blockchain Fundamentals\nWeek 2: Ethereum & EVM\nWeek 3: Solidity Basics\nWeek 4: Smart Contract Patterns\nWeek 5: Testing Smart Contracts\nWeek 6: dApp Frontend (ethers.js)\nWeek 7: DeFi Protocols\nWeek 8: Security & Capstone"),
        ("Statistics & Probability","Build the mathematical foundation for data science and ML: probability theory, distributions, hypothesis testing, Bayesian inference, and regression.","Prof. Elena Vasquez","Statistics professor at Cambridge, author of 3 textbooks","Mathematics","Beginner","7 weeks","https://www.youtube.com/embed/xxpc-HPKN28","statistics,probability,mathematics,data science,bayesian","Week 1: Descriptive Statistics\nWeek 2: Probability Theory\nWeek 3: Probability Distributions\nWeek 4: Hypothesis Testing\nWeek 5: Bayesian Inference\nWeek 6: Regression Analysis\nWeek 7: Applications & Capstone"),
        ("Django & REST APIs","Build production-grade web applications and RESTful APIs with Django and Django REST Framework. Covers authentication, serialisers, filtering, and deployment.","Omar Sheikh","Backend architect at Deliveroo, Django core contributor","Web Dev","Intermediate","9 weeks","https://www.youtube.com/embed/F5mRW0jo-U4","django,python,rest api,backend,postgresql,drf","Week 1-2: Django Fundamentals\nWeek 3: Models & ORM\nWeek 4: Views & Templates\nWeek 5: Django REST Framework\nWeek 6: Authentication & Permissions\nWeek 7: Filtering & Pagination\nWeek 8: Testing\nWeek 9: Deployment & Capstone"),
        ("Data Structures & Algorithms","Master the CS fundamentals every engineer needs: arrays, trees, graphs, dynamic programming, and sorting. Ace coding interviews at top tech companies.","Dr. Wei Liu","Former FAANG engineer, competitive programmer, LeetCode top 1%","Computer Science","Advanced","10 weeks","https://www.youtube.com/embed/8hly31xKli0","algorithms,data structures,leetcode,interviews,python,cs","Week 1: Arrays & Strings\nWeek 2: Linked Lists & Stacks\nWeek 3: Trees & Heaps\nWeek 4: Graphs & BFS/DFS\nWeek 5: Sorting & Searching\nWeek 6: Dynamic Programming\nWeek 7: Greedy Algorithms\nWeek 8: Advanced Graphs\nWeek 9: System Design\nWeek 10: Mock Interviews"),
    ]
    for c in courses:
        cur = db.execute(
            "INSERT INTO courses (title,description,instructor,instructor_bio,category,level,duration,video_url,tags,syllabus) VALUES (?,?,?,?,?,?,?,?,?,?)", c)
        cid = cur.lastrowid
        for i, w in enumerate([l.strip() for l in c[9].split('\n') if l.strip()]):
            db.execute("INSERT INTO lessons (course_id,title,position) VALUES (?,?,?)", (cid, w, i))

    pw = hash_password("admin123")
    db.execute("INSERT OR IGNORE INTO users (username,email,password_hash,is_admin,bio) VALUES (?,?,?,?,?)",
               ("admin","admin@learnsphere.com",pw,1,"Platform administrator"))

    # Seed announcements
    db.execute("INSERT INTO announcements (title,body,kind,created_by) VALUES (?,?,?,?)",
               ("Welcome to LearnSphere v2!",
                "We've launched a major upgrade: progress tracking, reviews, certificates, and 15 new courses. Enjoy learning!",
                "success", None))
    db.execute("INSERT INTO announcements (title,body,kind,created_by) VALUES (?,?,?,?)",
               ("New courses available",
                "Blockchain & Web3, Cybersecurity Fundamentals, iOS Development, Cloud Computing with AWS, and Data Structures & Algorithms are now live.",
                "info", None))
    db.commit()

# ── App factory ──────────────────────────────────────────────────────────────

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

    # Session security
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=3600,   # 1 hour timeout
    )

    app.teardown_appcontext(close_db)
    init_db(app)

    @app.context_processor
    def inject_globals():
        db = get_db()
        announcements = db.execute(
            "SELECT * FROM announcements ORDER BY created_at DESC LIMIT 3"
        ).fetchall()
        return dict(
            session=session,
            csrf_token=generate_csrf_token,
            announcements=announcements,
        )

    # Session timeout check
    @app.before_request
    def check_session_timeout():
        if session.get('user_id'):
            last = session.get('_last_active', 0)
            if time.time() - last > 3600:
                session.clear()
                return
            session['_last_active'] = time.time()

    # Security headers on every response
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "frame-src https://www.youtube.com; "
            "img-src 'self' data:;"
        )
        return response

    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.courses.routes import courses_bp
    from app.admin.routes import admin_bp
    from app.api.routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')


    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    return app

# Expose COURSE_CONTENT so templates can look up rich text
from app.course_content import COURSE_CONTENT
