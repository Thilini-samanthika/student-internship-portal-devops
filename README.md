# Student Internship Portal 

A full-stack web application for managing student internship applications, built with Flask (Python) backend and vanilla JavaScript frontend.

## 👥 Project Team Members

| Student ID      | Responsibility                                             |
| --------------- | ---------------------------------------------------------- |
| ITBIN-2313-0061 | DevOps (CI/CD, GitHub Actions, deployment support)         |
| ITBIN-2313-0081 | Frontend Development (UI, JavaScript, Bootstrap, Chart.js) |
| ITBIN-2313-0017 | Backend Development (Flask API, MySQL, JWT authentication) |


Features

 Core Features
- Internship Listings: Admin can post internships with details (title, company, description, duration, slots)
- Student Application: Students can apply for internships with CV upload and cover letter
- Application Validation: Prevents multiple applications for the same internship
- Admin Dashboard: Approve/reject applications and track statistics
- Status Tracking: Students can view their application status (Pending, Approved, Rejected)
- User Roles: Separate authentication for Admin and Student users

Advanced Features
- RESTful API: Clean API endpoints for frontend-backend communication
- JWT Authentication: Secure token-based authentication
- AJAX/Fetch API: Dynamic content updates without page reloads
- Modern UI: Responsive design with Bootstrap 5
- Statistics Dashboard: Charts using Chart.js for admin analytics
- GitHub Actions: Automated testing workflow

 Tech Stack

- Backend: Python (Flask), MySQL
- Frontend: HTML, CSS, JavaScript (Bootstrap 5, Chart.js)
- Authentication: JWT (JSON Web Tokens)
- Database: MySQL
- Version Control: GitHub + GitHub Actions

 Project Structure



├── backend/
│   ├── app.py                 - Flask application
│   ├── requirements.txt       - Python dependencies
│   ├── database_setup.sql     - Database schema
│   ├── test_api.py           -API tests
│   └── uploads/              - CV file uploads (created automatically)
├── frontend/
│   ├── index.html            - Home page
│   ├── login.html            - Login page
│   ├── register.html         - Registration page
│   ├── student-dashboard.html - Student dashboard
│   ├── internships.html      -Browse internships
│   ├── admin-dashboard.html  - Admin dashboard
│   ├── admin-internships.html - Manage internships
│   ├── admin-applications.html - Manage applications
│   ├── css/
│   │   └── style.css         -Custom styles
│   └── js/
│       ├── api.js            - API helper functions
│       ├── login.js          -- Login functionality
│       ├── register.js       -Registration functionality
│       ├── index.js          - Home page logic
│       ├── student-dashboard.js - Student dashboard
│       ├── internships.js    - Browse internships
│       ├── admin-dashboard.js - Admin dashboard
│       ├── admin-internships.js - Manage internships
│       └── admin-applications.js - Manage applications
└── .github/
    └── workflows/
        └── test.yml          - GitHub Actions workflow
```

Installation & Setup

 Prerequisites
- Python 3.9+
- MySQL 8.0+
- Node.js (optional, for local development server)

Backend Setup

1. Navigate to backend directory:
   bash
   cd backend
   

2. Create virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   

3. Install dependencies:
   bash
   pip install -r requirements.txt
   

4. Configure MySQL:
   - Create a MySQL database named `internship_portal`
   - Update database credentials in `app.py` (DB_CONFIG):
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'database': 'internship_portal',
         'user': 'root',
         'password': 'your_password'  # Change this
     }
     

5. Initialize database:
   - Option 1: Run the SQL script:
     bash
     mysql -u root -p < database_setup.sql
     
   - Option 2: The app will auto-create tables on first run

6. Run the Flask server:
   bash
   python app.py
   
   The API will be available at `http://localhost:5000`

 Frontend Setup

1. Navigate to frontend directory:
   bash
   cd frontend
   

2. Serve the frontend:
   - Option 1: Use Python's HTTP server:
     bash
     python -m http.server 8000
     
   - Option 2: Use Node.js http-server:
   bash
     npx http-server -p 8000
     
   - Option 3: Use any web server (Apache, Nginx, etc.)

3. Access the application:
   Open `http://localhost:8000` in your browser

 CORS Configuration

If you encounter CORS issues, make sure:
- Backend is running on `http://localhost:5000`
- Frontend is configured to use `http://localhost:5000/api` (see `frontend/js/api.js`)
 API Endpoints
 Authentication
- `POST /api/register/student` - Register a new student
- `POST /api/register/admin` - Register a new admin
- `POST /api/login` - Login (returns JWT token)
- `GET /api/me` - Get current user info (requires auth)

 Internships
- `GET /api/internships` - Get all internships
- `POST /api/internships` - Create internship (Admin only)

Applications
- `POST /api/apply` - Apply for internship (Student only)
- `GET /api/status` - Get application status (Student only)
- `GET /api/applications` - Get all applications (Admin only)
- `POST /api/applications/<id>/approve` - Approve application (Admin only)
- `POST /api/applications/<id>/reject` - Reject application (Admin only)

 Statistics
- `GET /api/stats` - Get dashboard statistics (Admin only)

 Usage

 For Students

1. Register: Create an account at `/register.html`
2. Login: Access your dashboard at `/login.html`
3. Browse Internships: View available internships
4. Apply: Submit applications with CV and cover letter
5. Track Status: View application status in your dashboard
 For Admins

1. Login: Use admin credentials to access admin panel
2. Create Internships: Post new internship opportunities
3. Manage Applications: Approve or reject student applications
4. View Statistics: Monitor application statistics and trends

 Default Admin Account

After running `database_setup.sql`, you can create an admin account using the API:

bash
curl -X POST http://localhost:5000/api/register/admin \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'


Or manually insert into the database (password will be hashed by the app).
 Testing

Manual Testing
1. Run the backend server
2. Test API endpoints using Postman or curl
3. Test frontend by navigating through all pages

 Automated Testing
GitHub Actions workflow runs on push/PR:
- Tests imports and basic functionality
- Validates API structure

Run tests locally:
bash
cd backend
python test_api.py

echo "Test auto-deploy" >> README.md


 Security Notes

Important for Production:
- Change `JWT_SECRET_KEY` in `app.py` to a secure random string
- Use environment variables for database credentials
- Implement rate limiting
- Add HTTPS/SSL
- Sanitize file uploads
- Implement proper error handling
- Add input validation and sanitization

File Uploads

- CV files are stored in `backend/uploads/`
- Allowed formats: PDF, DOC, DOCX
- Max file size: 16MB
- Files are renamed to prevent conflicts: `{student_id}_{internship_id}_{filename}`

Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

 License

This project is open source and available for educational purposes.

Support

For issues or questions, please open an issue on GitHub.

we are successfully Built with  for student internship management

