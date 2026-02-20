Student Internship Portal

A full-stack web application for managing student internship applications, built with Flask (Python) backend and vanilla JavaScript frontend.

Live Deployment

The Student Internship Portal is deployed and live at:
    https://web-production-6596b.up.railway.app

Project Team Members

About The Project
The Student Internship Portal is a modern web application designed to digitalize and simplify the internship management process between students and administrators.
Instead of manual processing, this system provides:
•	Online internship postings
•	Secure student applications
•	Admin approval system
•	Real-time status tracking
•	Analytics dashboard
This project demonstrates real-world full-stack architecture with secure authentication and API communication.
 Architecture Overview
Frontend (HTML, CSS, JavaScript, Bootstrap)
                ↓
        REST API (Flask Backend)
                ↓
MySQL Database

 Stateless JWT Authentication
 Role-Based Access Control
 Secure API Endpoints
 Clean Separation of Frontend & Backend

 Tech Stack
🔹 Backend
•	Python
•	Flask
•	MySQL
•	JWT (JSON Web Tokens)
🔹 Frontend
•	HTML5
•	CSS3
•	JavaScript (Vanilla JS)
•	Bootstrap 5
•	Chart.js
🔹 DevOps
•	GitHub
•	GitHub Actions (CI/CD)
•	Railway Cloud Deployment
 Core Features
   Student Panel
•	View available internships
•	Apply with CV upload
•	Submit cover letter
•	Prevent duplicate applications
•	Track application status
o	🟡 Pending
o	🟢 Approved
o	🔴 Rejected

 Admin Panel
•	Create internship listings
•	Manage available slots
•	View all student applications
•	Approve / Reject applications
•	View analytics dashboard
 Authentication & Security
•	JWT-based authentication
•	Password hashing
•	Protected admin routes
•	Backend validation
•	Duplicate application prevention
 Analytics Dashboard
•	Real-time internship statistics
•	Application trends
•	Chart.js data visualization
•	Interactive admin insights
 Database Structure
Main Tables:
•	Users
•	Internships
•	Applications
Relationships:
•	One User → Many Applications
•	One Internship → Many Applications
 Installation Guide
1️⃣ Clone Repository
git clone https://github.com/your-username/student-internship-portal.git
cd student-internship-portal
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables
Create .env file:
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
5️⃣ Run the Application
flask run
🔁 CI/CD Workflow
✔ Automated GitHub Actions pipeline
✔ Code testing on every push
✔ Continuous deployment to Railway
✔ Improved reliability & collaboration


| Student ID                         | Responsibility                                             |
| ---------------                    | ---------------------------------------------------------- |
| ITBIN-2313-0061-M.T.Samanthika     | DevOps (CI/CD, GitHub Actions, deployment support)         |
| ITBIN-2313-0081-P.A.C.S.P Arewwala | Frontend Development (UI, JavaScript, Bootstrap, Chart.js) |
| ITBIN-2313-0017 -D.H.M.H.M.Herath  | Backend Development (Flask API, MySQL, JWT authentication) |


