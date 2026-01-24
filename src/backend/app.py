from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import mysql.connector
from mysql.connector import Error
from functools import wraps
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

jwt = JWTManager(app)
CORS(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'internship_portal',
    'user': 'root',
    'password': 'Thilini12345'  
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database tables"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                course VARCHAR(255),
                year INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internships (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                description TEXT,
                duration VARCHAR(100),
                slots INT DEFAULT 0,
                date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                admin_id INT,
                FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE SET NULL
            )
        """)
        
        # Create applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                internship_id INT NOT NULL,
                cv_file VARCHAR(255),
                cover_letter TEXT,
                status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
                UNIQUE KEY unique_application (student_id, internship_id)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully!")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE id = %s", (current_user['id'],))
            admin = cursor.fetchone()
            cursor.close()
            connection.close()
            if not admin:
                return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator to require student role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE id = %s", (current_user['id'],))
            student = cursor.fetchone()
            cursor.close()
            connection.close()
            if not student:
                return jsonify({'error': 'Student access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Authentication Routes
@app.route('/api/register/student', methods=['POST'])
def register_student():
    """Register a new student"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM students WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password and insert student
    hashed_password = generate_password_hash(data['password'])
    cursor.execute("""
        INSERT INTO students (name, email, password, course, year)
        VALUES (%s, %s, %s, %s, %s)
    """, (data.get('name'), data['email'], hashed_password, data.get('course'), data.get('year')))
    
    connection.commit()
    student_id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Student registered successfully', 'student_id': student_id}), 201

@app.route('/api/register/admin', methods=['POST'])
def register_admin():
    """Register a new admin (usually done manually)"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM admins WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password and insert admin
    hashed_password = generate_password_hash(data['password'])
    cursor.execute("""
        INSERT INTO admins (name, email, password)
        VALUES (%s, %s, %s)
    """, (data.get('name'), data['email'], hashed_password))
    
    connection.commit()
    admin_id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Admin registered successfully', 'admin_id': admin_id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login for both students and admins"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    # Check student table
    cursor.execute("SELECT * FROM students WHERE email = %s", (data['email'],))
    user = cursor.fetchone()
    role = 'student'
    
    # If not found, check admin table
    if not user:
        cursor.execute("SELECT * FROM admins WHERE email = %s", (data['email'],))
        user = cursor.fetchone()
        role = 'admin'
    
    cursor.close()
    connection.close()
    
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create access token
    access_token = create_access_token(identity={
        'id': user['id'],
        'email': user['email'],
        'role': role
    })
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': role
        }
    }), 200

# Internship Routes
@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get all available internships"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.*, a.name as admin_name,
               (SELECT COUNT(*) FROM applications WHERE internship_id = i.id) as applications_count
        FROM internships i
        LEFT JOIN admins a ON i.admin_id = a.id
        ORDER BY i.date_posted DESC
    """)
    internships = cursor.fetchall()
    
    # Convert datetime to string for JSON serialization
    for internship in internships:
        if internship['date_posted']:
            internship['date_posted'] = internship['date_posted'].isoformat()
    
    cursor.close()
    connection.close()
    
    return jsonify(internships), 200

@app.route('/api/internships', methods=['POST'])
@admin_required
def create_internship():
    """Create a new internship (Admin only)"""
    data = request.get_json()
    current_user = get_jwt_identity()
    
    if not data or not data.get('title') or not data.get('company'):
        return jsonify({'error': 'Title and company are required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO internships (title, company, description, duration, slots, admin_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['title'], data['company'], data.get('description'), 
          data.get('duration'), data.get('slots', 0), current_user['id']))
    
    connection.commit()
    internship_id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Internship created successfully', 'internship_id': internship_id}), 201

# Application Routes
@app.route('/api/apply', methods=['POST'])
@student_required
def apply_internship():
    """Apply for an internship (Student only)"""
    current_user = get_jwt_identity()
    student_id = current_user['id']
    
    # Check if application data is provided
    if 'internship_id' not in request.form:
        return jsonify({'error': 'Internship ID is required'}), 400
    
    internship_id = request.form['internship_id']
    cover_letter = request.form.get('cover_letter', '')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    
    # Check if already applied
    cursor.execute("""
        SELECT * FROM applications 
        WHERE student_id = %s AND internship_id = %s
    """, (student_id, internship_id))
    
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({'error': 'You have already applied for this internship'}), 400
    
    # Handle file upload
    cv_file = None
    if 'cv_file' in request.files:
        file = request.files['cv_file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{student_id}_{internship_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            cv_file = filename
    
    # Insert application
    cursor.execute("""
        INSERT INTO applications (student_id, internship_id, cv_file, cover_letter, status)
        VALUES (%s, %s, %s, %s, 'Pending')
    """, (student_id, internship_id, cv_file, cover_letter))
    
    connection.commit()
    application_id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Application submitted successfully', 'application_id': application_id}), 201

@app.route('/api/status', methods=['GET'])
@student_required
def get_application_status():
    """Get application status for logged-in student"""
    current_user = get_jwt_identity()
    student_id = current_user['id']
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, i.title, i.company, i.description
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        WHERE a.student_id = %s
        ORDER BY a.applied_at DESC
    """, (student_id,))
    
    applications = cursor.fetchall()
    
    # Convert datetime to string
    for app in applications:
        if app['applied_at']:
            app['applied_at'] = app['applied_at'].isoformat()
    
    cursor.close()
    connection.close()
    
    return jsonify(applications), 200

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)