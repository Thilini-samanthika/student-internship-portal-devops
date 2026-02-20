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
| ITBIN-2313-0017-D.H.M.H.M.Herath   | Backend Development (Flask API, MySQL, JWT authentication) |

Tech Stack

* Backend: Python (Flask), MySQL
* Frontend: HTML, CSS, JavaScript (Bootstrap 5, Chart.js)
* Authentication: JWT (JSON Web Tokens)
* Version Control: GitHub + GitHub Actions

 Features

Core Features

* Internship Listings: Admin can post internships with details (title, company, description, duration, slots)
* Student Application: Students can apply for internships with CV upload and cover letter
* Application Validation: Prevents multiple applications for the same internship
* Admin Dashboard: Approve/reject applications and track statistics
* Status Tracking: Students can view their application status (Pending, Approved, Rejected)
* User Roles: Separate authentication for Admin and Student users

Advanced Features

* RESTful API: Clean API endpoints for frontend-backend communication
* JWT Authentication: Secure token-based authentication
* AJAX/Fetch API: Dynamic content updates without page reloads
* Modern UI: Responsive design with Bootstrap 5
* Statistics Dashboard: Charts using Chart.js for admin analytics
* GitHub Actions: Automated testing workflow

Installation Guide

 * Clone Repository
   
       git clone https://github.com/your-username/student-internship-portal.git
   
       cd student-internship-portal
   
 * Create Virtual Environment
   
       python -m venv venv
   
       source venv/bin/activate
      
       Windows: venv\Scripts\activate
   
 * Install Dependencies
   
        pip install -r requirements.txt
   
 * Setup Environment Variables
   
      Create .env file:
   
        SECRET_KEY=your_secret_key
        DATABASE_URL=your_database_url
        JWT_SECRET_KEY=your_jwt_secret
   
 * Run the Application
   
        flask run
   
 * CI/CD Workflow
   
     Automated GitHub Actions pipeline
   
     Code testing on every push
   
     Continuous deployment to Railway
   
     Improved reliability & collaboration
