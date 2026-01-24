from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import mysql.connector
from mysql.connector import Error
from functools import wraps

# ------------------ APP CONFIG ------------------

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ.get(
    "JWT_SECRET_KEY", "dev-secret-key"
)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

jwt = JWTManager(app)

# ------------------ DATABASE CONFIG ------------------

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("Thilini12345"),
    "database": os.environ.get("internship_portal"),
    "port": int(os.environ.get("DB_PORT", 3306))
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("DB ERROR:", e)
        return None

# ------------------ HELPERS ------------------

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB error"}), 500

        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id FROM admins WHERE id=%s", (user["id"],))
        admin = cur.fetchone()
        cur.close()
        conn.close()

        if not admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper

def student_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB error"}), 500

        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id FROM students WHERE id=%s", (user["id"],))
        student = cur.fetchone()
        cur.close()
        conn.close()

        if not student:
            return jsonify({"error": "Student access required"}), 403
        return f(*args, **kwargs)
    return wrapper

# ------------------ AUTH ROUTES ------------------

@app.route("/api/register/student", methods=["POST"])
def register_student():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    cur = conn.cursor()
    cur.execute("SELECT id FROM students WHERE email=%s", (data["email"],))
    if cur.fetchone():
        return jsonify({"error": "Email exists"}), 400

    hashed = generate_password_hash(data["password"])
    cur.execute(
        "INSERT INTO students (name,email,password,course,year) VALUES (%s,%s,%s,%s,%s)",
        (data.get("name"), data["email"], hashed, data.get("course"), data.get("year"))
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student registered"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB error"}), 500

    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE email=%s", (data["email"],))
    user = cur.fetchone()
    role = "student"

    if not user:
        cur.execute("SELECT * FROM admins WHERE email=%s", (data["email"],))
        user = cur.fetchone()
        role = "admin"

    cur.close()
    conn.close()

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity={
        "id": user["id"],
        "email": user["email"],
        "role": role
    })

    return jsonify({"access_token": token, "role": role}), 200

# ------------------ BASIC TEST ROUTE ------------------

@app.route("/")
def health():
    return jsonify({"status": "Flask API running on Render"}), 200

# ------------------ RUN APP ------------------

<<<<<<< HEAD
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
=======
@app.route('/api/applications', methods=['GET'])
@admin_required
def get_all_applications():
    """Get all applications (Admin only)"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, s.name as student_name, s.email as student_email, s.course, s.year,
               i.title, i.company
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN internships i ON a.internship_id = i.id
        ORDER BY a.applied_at DESC
    """)
    
    applications = cursor.fetchall()
    
    # Convert datetime to string
    for app in applications:
        if app['applied_at']:
            app['applied_at'] = app['applied_at'].isoformat()
    
    cursor.close()
    connection.close()
    
    return jsonify(applications), 200

@app.route('/api/applications/<int:application_id>/approve', methods=['POST'])
@admin_required
def approve_application(application_id):
    """Approve an application (Admin only)"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE applications 
        SET status = 'Approved'
        WHERE id = %s
    """, (application_id,))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Application approved successfully'}), 200

@app.route('/api/applications/<int:application_id>/reject', methods=['POST'])
@admin_required
def reject_application(application_id):
    """Reject an application (Admin only)"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE applications 
        SET status = 'Rejected'
        WHERE id = %s
    """, (application_id,))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Application rejected successfully'}), 200

@app.route('/api/stats', methods=['GET'])
@admin_required
def get_statistics():
    """Get dashboard statistics (Admin only)"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    # Total internships
    cursor.execute("SELECT COUNT(*) as total FROM internships")
    total_internships = cursor.fetchone()['total']
    
    # Total applications
    cursor.execute("SELECT COUNT(*) as total FROM applications")
    total_applications = cursor.fetchone()['total']
    
    # Pending applications
    cursor.execute("SELECT COUNT(*) as total FROM applications WHERE status = 'Pending'")
    pending_applications = cursor.fetchone()['total']
    
    # Approved applications
    cursor.execute("SELECT COUNT(*) as total FROM applications WHERE status = 'Approved'")
    approved_applications = cursor.fetchone()['total']
    
    # Rejected applications
    cursor.execute("SELECT COUNT(*) as total FROM applications WHERE status = 'Rejected'")
    rejected_applications = cursor.fetchone()['total']
    
    # Total students
    cursor.execute("SELECT COUNT(*) as total FROM students")
    total_students = cursor.fetchone()['total']
    
    cursor.close()
    connection.close()
    
    return jsonify({
        'total_internships': total_internships,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'total_students': total_students
    }), 200

@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user information"""
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

handler = Mangum(app)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
>>>>>>> bb5cc12 (Resolve merge conflicts)
