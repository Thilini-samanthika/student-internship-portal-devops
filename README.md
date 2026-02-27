# Student Internship Portal

A full-stack web application for managing student internship applications, built with Flask (Python) backend and Vanilla JavaScript frontend.
This project demonstrates real-world Git workflow, CI/CD automation, and cloud deployment practices.

## Group Information

Student 1: M.T. Samanthika - ITBIN-2313-0061 - Role: DevOps Engineer

Student 2: P.A.C.S.P. Arewwala - ITBIN-2313-0081 - Role: Frontend Developer

Student 3: D.H.M.H.M. Herath - ITBIN-2313-0017 - Role: Backend Developer

## Live Deployment

### Live URL:
https://thilinisamanthika.pythonanywhere.com/

## Technologies Used

#### Backend

- Python

- Flask

- MySQL

- JWT Authentication

#### Frontend

- HTML5

- CSS3

- JavaScript (ES6)

- Bootstrap 5

- Chart.js

#### DevOps

- Git & GitHub

- GitHub Actions (CI/CD)

- PythonAnywhere (Cloud Deployment)

## Features
#### Core Features

 - Internship listings management (Admin)

 - Student internship application system

 - CV upload and cover letter submission

 - Duplicate application prevention

- Admin dashboard for approving/rejecting applications

- Application status tracking (Pending / Approved / Rejected)

- Role-based authentication (Admin & Student)

#### Advanced Features

 - RESTful API architecture

 - Secure JWT token-based authentication

 - AJAX / Fetch API integration

 - Fully responsive UI (Bootstrap 5)

 - Admin analytics dashboard (Chart.js)

 - Automated CI/CD pipeline using GitHub Actions

## Branch Strategy

We implemented a professional Git workflow:

 - main – Production branch (auto-deployed)

 - develop – Integration branch

 - feature/* – Individual feature branches

All changes were merged using Pull Requests after review.

## Setup Instructions
Prerequisites

- Python 3.10+

- MySQL

- Git

##### 1️ Clone the Repository
git clone https://github.com/Thilini-samanthika/student-internship-portal.git
cd student-internship-portal
##### 2️ Create Virtual Environment
python -m venv venv

Activate:

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
##### 3️ Install Dependencies
pip install -r src/backend/requirements.txt
##### 4️ Configure Environment Variables

Create a .env file:

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
##### 5️ Run the Application
flask run

Application runs at:

http://127.0.0.1:5000
- CI/CD Workflow

This project uses GitHub Actions for automated Continuous Integration and Continuous Deployment.

## Continuous Integration (CI)

- Triggered on:

Push to main, develop, feature/*

Pull requests to main and develop

- CI Process:

Checkout repository

Setup Python environment

Install dependencies

Run backend tests

Verify build integrity

This ensures code quality before merging.

## Continuous Deployment (CD)

- Triggered when:

Code is merged/pushed into main

- Deployment Platform:

PythonAnywhere

- Deployment Process:

GitHub Actions verifies tests

Production branch updates

PythonAnywhere web application reloads

Live site updates automatically

- Secrets used (GitHub → Settings → Secrets):

PA_USERNAME

PA_API_TOKEN

PA_DOMAIN_NAME

## Individual Contributions
 - M.T. Samanthika (DevOps Engineer)

     - Repository setup and configuration

     - Git branching strategy implementation

     - GitHub Actions CI/CD setup

     - PythonAnywhere deployment configuration

     - Merge conflict resolution

     - Production release management

 - P.A.C.S.P. Arewwala (Frontend Developer)

    - UI/UX implementation

    - JavaScript logic development

    - Bootstrap styling

    - Chart.js dashboard integration

    - Responsive design implementation

 - D.H.M.H.M. Herath (Backend Developer)

    - Flask REST API development

    - MySQL database integration

    - JWT authentication system

    - Application validation logic

    - Role-based access control

## Challenges Faced

Secure JWT authentication implementation

Preventing duplicate internship applications

Role-based authorization logic

CI/CD pipeline configuration

Environment variable management in production

 ## Solutions Implemented

Middleware-based token validation

Backend validation logic for duplicate prevention

Structured Git workflow with feature branches

Automated testing before deployment

Secure environment configuration via secrets



