# Student Record Management API

## Overview

The Student Record Management API is a backend application developed using FastAPI, SQLAlchemy, and MySQL. The project provides RESTful APIs to manage student records through CRUD (Create, Read, Update, Delete) operations.

This project demonstrates database integration, API development, data validation, and dynamic routing in a real-world backend application.

---

## Features

* Create a new student record
* View all student records
* View a specific student using Student ID
* Update student details
* Delete student records
* Input validation using Pydantic
* Database integration using SQLAlchemy ORM
* Dynamic routing with FastAPI
* Interactive API documentation using Swagger UI

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* Uvicorn

---

## Project Structure

student-management-api/

├── app/

│   ├── main.py

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   └── crud.py

├── requirements.txt

└── README.md

---

## Installation

### Clone the Repository

git clone <repository-url>

cd student-management-api

### Install Dependencies

pip install -r requirements.txt

---

## Database Configuration

Create a MySQL database:

CREATE DATABASE student_db;

Update the database connection string inside `database.py`:

DATABASE_URL = "mysql+pymysql://username:password@localhost/student_db"

---

## Run the Application

python -m uvicorn app.main:app --reload

Server will start at:

http://127.0.0.1:8000

---

## API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

---

## API Endpoints

### Create Student

POST /students/

Creates a new student record.

### Get All Students

GET /students/

Returns all student records.

### Get Student By ID

GET /students/{student_id}

Returns a specific student record.

### Update Student

PUT /students/{student_id}

Updates an existing student record.

### Delete Student

DELETE /students/{student_id}

Deletes a student record.

---

## Student Model

| Field  | Type    |
| ------ | ------- |
| id     | Integer |
| name   | String  |
| age    | Integer |
| email  | String  |
| course | String  |

---

## Learning Outcomes

Through this project, the following concepts were implemented:

* FastAPI application development
* REST API design
* CRUD operations
* SQLAlchemy ORM integration
* MySQL database connectivity
* Pydantic data validation
* Dynamic routing
* API testing using Swagger UI

---

## Author

Archismita Das

Backend Development Internship Project
