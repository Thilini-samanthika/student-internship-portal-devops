Student Internship Portal

A full-stack web application for managing student internship applications, built with Flask (Python) backend and vanilla JavaScript frontend.

Live Deployment

The Student Internship Portal is deployed and live at:
    https://web-production-6596b.up.railway.app

Project Team Members

| Student ID                         | Responsibility                                             |
| ---------------                    | ---------------------------------------------------------- |
| ITBIN-2313-0061-M.T.Samanthika     | DevOps (CI/CD, GitHub Actions, deployment support)         |
| ITBIN-2313-0081-P.A.C.S.P Arewwala | Frontend Development (UI, JavaScript, Bootstrap, Chart.js) |
| ITBIN-2313-0017 -D.H.M.H.M.Herath  | Backend Development (Flask API, MySQL, JWT authentication) |

Project Overview

The Student Internship Portal streamlines the internship application process between students and administrators.

It allows:

Students to browse internships and apply online

Admins to manage internship postings

Real-time tracking of applications

Secure authentication with JWT

Analytics dashboard for monitoring statistics

System Architecture
Frontend (HTML, CSS, JS, Bootstrap)
        ↓
REST API (Flask Backend)
        ↓
MySQL Database

Stateless authentication using JWT

RESTful API communication via Fetch/AJAX

Secure backend validation

Role-based route protection

Tech Stack
🔹 Backend

Python 3

Flask

MySQL

JWT Authentication

🔹 Frontend

HTML5

CSS3

JavaScript (Vanilla JS)

Bootstrap 5

Chart.js

🔹 DevOps

GitHub

GitHub Actions (CI/CD)

Railway (Cloud Deployment)

    Features
    Authentication & Authorization

JWT-based login system

Role-based access control (Admin / Student)

Protected API routes

Student Features

View available internships

Apply with CV upload

Submit cover letter

Track application status (Pending / Approved / Rejected)

Prevent duplicate applications

Admin Features

Create internship listings

Manage available slots

View all applications

Approve or reject students

Dashboard with statistical charts

Analytics Dashboard

Internship application statistics

Real-time data visualization

Chart.js integration

RESTful API Design
Method	Endpoint	Description
POST	/register	User registration
POST	/login	User authentication
GET	/internships	Get all internships
POST	/apply	Apply for internship
PUT	/applications/:id	Update application status
Database Design

Main Tables:

Users

Internships

Applications

Relationships:

One User → Many Applications

One Internship → Many Applications

Installation & Setup
1️⃣Clone Repository
git clone https://github.com/your-username/student-internship-portal.git
cd student-internship-portal
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create .env file:

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
5️⃣ Run Application
flask run
CI/CD Pipeline

Automated workflow using GitHub Actions

Code testing on push

Continuous deployment to Railway

Improved reliability and collaboration

Security Implementation

JWT Token Expiry

Password Hashing

Backend Input Validation

Protected Admin Routes

Duplicate Application Prevention Logic
