#  Student Internship Portal

A full-stack web application for managing student internship applications, built with **Flask (Python)** backend and **Vanilla JavaScript** frontend.

---

##  Live Deployment

🔗 **Live URL**  
https://web-production-6596b.up.railway.app

---

##  Project Team Members

| Student ID | Name | Role | Responsibility |
|------------|------|------|----------------|
| ITBIN-2313-0061 | M.T. Samanthika | DevOps Engineer | CI/CD pipeline, GitHub Actions, deployment |
| ITBIN-2313-0081 | P.A.C.S.P. Arewwala | Frontend Developer | UI design, JavaScript logic, Bootstrap, Chart.js |
| ITBIN-2313-0017 | D.H.M.H.M. Herath | Backend Developer | Flask API, MySQL database, JWT authentication |

---

##  Tech Stack

### Backend
- Python
- Flask
- MySQL
- JWT Authentication

### Frontend
- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5
- Chart.js

### DevOps
- GitHub
- GitHub Actions (CI/CD)
- Railway (Deployment)

---

##  Features

### Core Features
- Internship listings management (Admin)
- Student internship application system
- CV upload and cover letter submission
- Application validation (prevents duplicate applications)
- Admin dashboard for approving/rejecting applications
- Application status tracking (Pending / Approved / Rejected)
- Role-based authentication (Admin & Student)

### Advanced Features
- RESTful API architecture
- Secure JWT token-based authentication
- AJAX / Fetch API for dynamic updates
- Fully responsive UI using Bootstrap 5
- Admin analytics dashboard using Chart.js
- Automated CI/CD pipeline with GitHub Actions

---

##  Branch Strategy

The following Git branching strategy was used:

- `main` – Production-ready code
- `develop` – Integration and testing branch
- `feature/*` – Individual feature development branches

---

##  Setup Instructions

### Prerequisites
- Python 3.10 or higher
- MySQL
- Git

---

##  Installation

### 1️ Clone the Repository

git clone https://github.com/Thilini-samanthika/student-internship-portal.git
cd student-internship-portal

### 2️ Create Virtual Environment
python -m venv venv

Activate the virtual environment:
Mac / Linux
source venv/bin/activate

Windows
venv\Scripts\activate

### 3 Install Dependencies
pip install -r requirements.txt

### 4️ Setup Environment Variables
Create a .env file in the root directory and add:

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret

### 5 Run the Application
flask run

The application will be available at:

http://127.0.0.1:5000

### CI/CD Workflow

This project uses GitHub Actions for Continuous Integration and Continuous Deployment.

Workflow Process

  - Code push to the develop branch triggers the CI workflow

  - Automated tests are executed

  - If tests pass, the application is deployed to Railway

  - Production environment is updated automatically

Benefits

  - Reliable and consistent deployments

  - Faster team collaboration

  - Reduced manual deployment errors

Challenges Faced

  - Secure implementation of JWT authentication

  - Preventing multiple applications for the same internship

  - Managing role-based access control

  - Configuring environment variables for Railway deployment

Solutions Implemented

  - Token validation middleware

  - Backend validation logic

  - Well-structured Git branching strategy

  - Secure .env configuration management
