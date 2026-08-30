# Student Management System

A full-stack Student Management System built using **FastAPI, SQLAlchemy, MySQL, HTML, CSS, and JavaScript**.

The project started as a basic CRUD API and was upgraded into an intermediate-level application with a web frontend, validation, search, filtering, pagination, and proper database integration.

## Features

- Create, view, update, and delete students
- Search students by name, email, or course
- Filter by course, department, and semester
- Pagination for student records
- Duplicate email prevention
- Input validation and error handling
- Dashboard with total student count
- Responsive frontend
- FastAPI Swagger API documentation
- MySQL database integration using SQLAlchemy

## Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- Uvicorn
- python-dotenv

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API

## Architecture

```text
Frontend (HTML/CSS/JavaScript)
            |
          fetch()
            |
            v
       FastAPI REST API
            |
            v
        CRUD Layer
            |
            v
       SQLAlchemy ORM
            |
            v
       MySQL Database
Request Flow
The frontend sends a request using JavaScript fetch().
FastAPI receives the request through the appropriate route.
Pydantic validates the request data.
The CRUD layer handles database operations.
SQLAlchemy communicates with MySQL.
The result is returned as JSON to the frontend.
Project Structure
student-management-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       └── students.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
Database Setup

Make sure MySQL Server is installed and running.

Create the database:

CREATE DATABASE student_db;

The required tables are created automatically by SQLAlchemy when the application starts.

Environment Configuration

Create a .env file in the project root using .env.example as a template.

DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_db

Do not commit .env to GitHub.

Installation

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Run the Application

Start the FastAPI server:

uvicorn app.main:app --reload

The application will be available at:

http://127.0.0.1:8000/

The frontend is served directly by FastAPI, so no separate frontend server is required.

Swagger API Documentation

FastAPI automatically provides interactive API documentation at:

http://127.0.0.1:8000/docs
API Endpoints
Method	Endpoint	Description
POST	/students/	Create a student
GET	/students/	List students
GET	/students/{id}	Get a student
PUT	/students/{id}	Update a student
DELETE	/students/{id}	Delete a student
GET /students/ Query Parameters
Parameter	Type	Description
search	string	Search by name, email, or course
course	string	Filter by course
department	string	Filter by department
semester	integer	Filter by semester
skip	integer	Number of records to skip
limit	integer	Maximum records to return
Student Data

Each student record contains:

id
name
age
email
phone
course
department
semester

Example request:

{
  "name": "Alex Roy",
  "age": 20,
  "email": "alex@example.com",
  "phone": "9876543210",
  "course": "Computer Science",
  "department": "CSE",
  "semester": 3
}
Screenshots
Student Dashboard

Add project screenshot here.

Add / Edit Student

Add project screenshot here.

Future Improvements
Authentication and role-based access
CSV import/export
Sortable table columns
Automated testing with pytest
Audit fields such as created_at and updated_at
Cloud deployment
Author

Archismita Das
