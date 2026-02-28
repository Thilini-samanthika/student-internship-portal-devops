from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import sqlite3
import json

from functools import wraps
from dotenv import load_dotenv

load_dotenv()

# APP CONFIG

BASE_DIR = os.path.dirname(__file__)                 
SRC_DIR = os.path.dirname(BASE_DIR)                  
FRONTEND_FOLDER = os.path.join(SRC_DIR, "frontend")  
UPLOAD_FOLDER = os.path.join(FRONTEND_FOLDER, "uploads")

app = Flask(__name__, static_folder=FRONTEND_FOLDER, static_url_path="")
CORS(app)

#JWT
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

if not app.config["SECRET_KEY"] or not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY and JWT_SECRET_KEY must be set as environment variables")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Uploads
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

jwt = JWTManager(app)

#DATABASE CONFIG

DEFAULT_DB_FILE = os.path.join(BASE_DIR, "internship_portal.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_FILE}")

def _sqlite_path_from_url(db_url: str) -> str:
    """
    Convert sqlite URL to filesystem path.

    sqlite:////abs/path.db  -> /abs/path.db
    sqlite:///rel/path.db   -> rel/path.db
    """
    if not db_url.startswith("sqlite:///"):
        raise ValueError("Unsupported DB. Only sqlite:/// is supported in this project.")
    return db_url.replace("sqlite:///", "", 1)

def get_db_connection():
    try:
        db_path = _sqlite_path_from_url(DATABASE_URL)
        # Ensure parent folder exists (useful in docker volumes)
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to DB during initialization.")
        return

    schema_queries = [
        """CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            course TEXT,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT,
            duration TEXT,
            slots INTEGER DEFAULT 0,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            admin_id INTEGER,
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        )""",
        """CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            internship_id INTEGER NOT NULL,
            cv_file TEXT,
            cover_letter TEXT,
            status TEXT DEFAULT 'Pending',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (internship_id) REFERENCES internships(id),
            UNIQUE(student_id, internship_id)
        )"""
    ]

    try:
        cur = conn.cursor()
        for query in schema_queries:
            cur.execute(query)

        # Default admin
        email = "admin@example.com"
        cur.execute("SELECT id FROM admins WHERE email = ?", (email,))
        if not cur.fetchone():
            hashed_password = generate_password_hash("admin123")
            cur.execute(
                "INSERT INTO admins (name, email, password) VALUES (?, ?, ?)",
                ("Admin User", email, hashed_password)
            )
            print("Default admin created: admin@example.com / admin123")

        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing DB:", e)

# HELPERS

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def dict_from_row(row):

    if row is None:
        return None
    
    return dict(row)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = json.loads(get_jwt_identity())
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB error"}), 500

        try:

            cur = conn.cursor()
            cur.execute("SELECT id FROM admins WHERE id = ?", (user["id"],))
            admin = cur.fetchone()
            cur.close()
            conn.close()

            if not admin:
                return jsonify({"error": "Admin access required"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper

def student_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = json.loads(get_jwt_identity())
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB error"}), 500

        try:

            cur = conn.cursor()
            cur.execute("SELECT id FROM students WHERE id = ?", (user["id"],))
            student = cur.fetchone()
            cur.close()
            conn.close()

            if not student:
                return jsonify({"error": "Student access required"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper


#STATIC ROUTES


@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    full_path = os.path.join(app.static_folder, path)
    if os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


#API ROUTES


@app.route("/api/register/student", methods=["POST"])
def register_student():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM students WHERE email = ?", (data["email"],))
        if cur.fetchone():
            return jsonify({"error": "Email already exists"}), 400

        hashed = generate_password_hash(data["password"])
        cur.execute(
            "INSERT INTO students (name, email, password, course, year) VALUES (?, ?, ?, ?, ?)",
            (data.get("name"), data["email"], hashed, data.get("course"), data.get("year"))
        )
        conn.commit()
        return jsonify({"message": "Student registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/register/admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM admins WHERE email = ?", (data["email"],))
        if cur.fetchone():
            return jsonify({"error": "Email already exists"}), 400

        hashed = generate_password_hash(data["password"])
        cur.execute(
            "INSERT INTO admins (name, email, password) VALUES (?, ?, ?)",
            (data.get("name"), data["email"], hashed)
        )
        conn.commit()
        return jsonify({"message": "Admin registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email/password"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE email = ?", (data["email"],))
        user_row = cur.fetchone()
        user = dict_from_row(user_row)
        role = "student"

        if not user:
            cur.execute("SELECT * FROM admins WHERE email = ?", (data["email"],))
            user_row = cur.fetchone()
            user = dict_from_row(user_row)
            role = "admin"

        if not user or not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=json.dumps({"id": user["id"], "email": user["email"], "role": role}))
        return jsonify({"access_token": token, "role": role}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/internships", methods=["GET"])
def get_internships():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM internships ORDER BY date_posted DESC")
        internships = [dict_from_row(row) for row in cur.fetchall()]
        return jsonify(internships), 200
    finally:
        conn.close()

@app.route("/api/internships", methods=["POST"])
@admin_required
def create_internship():
    data = request.get_json() or {}
    user = json.loads(get_jwt_identity())

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO internships (title, company, description, duration, slots, admin_id) VALUES (?, ?, ?, ?, ?, ?)",
            (data.get("title"), data.get("company"), data.get("description"), data.get("duration"), data.get("slots", 0), user["id"])
        )
        conn.commit()
        return jsonify({"message": "Internship created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/apply", methods=["POST"])
@student_required
def apply_for_internship():
    user = json.loads(get_jwt_identity())
    internship_id = request.form.get("internship_id")
    cover_letter = request.form.get("cover_letter", "")
    cv_file = request.files.get("cv")

    if not internship_id:
        return jsonify({"error": "Internship ID required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM applications WHERE student_id = ? AND internship_id = ?",
            (user["id"], internship_id)
        )
        if cur.fetchone():
            return jsonify({"error": "Already applied"}), 400

        cv_filename = None
        if cv_file and allowed_file(cv_file.filename):
            filename = secure_filename(cv_file.filename)
            cv_filename = f"{user['id']}_{internship_id}_{filename}"
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            cv_file.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_filename))

        cur.execute(
            "INSERT INTO applications (student_id, internship_id, cv_file, cover_letter) VALUES (?, ?, ?, ?)",
            (user["id"], internship_id, cv_filename, cover_letter)
        )
        conn.commit()
        return jsonify({"message": "Application submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/status", methods=["GET"])
@student_required
def get_student_applications():
    user = json.loads(get_jwt_identity())
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, i.title, i.company
            FROM applications a
            JOIN internships i ON a.internship_id = i.id
            WHERE a.student_id = ?
            ORDER BY a.applied_at DESC
        """, (user["id"],))
        applications = [dict_from_row(row) for row in cur.fetchall()]
        return jsonify(applications), 200
    finally:
        conn.close()

@app.route("/api/applications", methods=["GET"])
@admin_required
def get_all_applications():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, s.name as student_name, s.email as student_email, s.course, s.year,
                   i.title, i.company
            FROM applications a
            JOIN students s ON a.student_id = s.id
            JOIN internships i ON a.internship_id = i.id
            ORDER BY a.applied_at DESC
        """)
        applications = [dict_from_row(row) for row in cur.fetchall()]
        return jsonify(applications), 200
    finally:
        conn.close()

@app.route("/api/applications/<int:application_id>/approve", methods=["POST"])
@admin_required
def approve_application(application_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("UPDATE applications SET status = 'Approved' WHERE id = ?", (application_id,))
        conn.commit()
        return jsonify({"message": "Application approved successfully"}), 200
    finally:
        conn.close()

@app.route("/api/applications/<int:application_id>/reject", methods=["POST"])
@admin_required
def reject_application(application_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    try:
        cur = conn.cursor()
        cur.execute("UPDATE applications SET status = 'Rejected' WHERE id = ?", (application_id,))
        conn.commit()
        return jsonify({"message": "Application rejected successfully"}), 200
    finally:
        conn.close()

@app.route("/api/stats", methods=["GET"])
@admin_required
def get_statistics():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    def get_count(cur, query, params=()):
        cur.execute(query, params)
        res = cur.fetchone()
        return res[0] if res else 0

    try:
        cur = conn.cursor()

        return jsonify({
            "total_internships": get_count(cur, "SELECT COUNT(*) FROM internships"),
            "total_applications": get_count(cur, "SELECT COUNT(*) FROM applications"),
            "pending_applications": get_count(cur, "SELECT COUNT(*) FROM applications WHERE status = 'Pending'"),
            "approved_applications": get_count(cur, "SELECT COUNT(*) FROM applications WHERE status = 'Approved'"),
            "rejected_applications": get_count(cur, "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"),
            "total_students": get_count(cur, "SELECT COUNT(*) FROM students"),
        }), 200
    finally:
        conn.close()


@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_current_user():
    return jsonify(json.loads(get_jwt_identity())), 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)