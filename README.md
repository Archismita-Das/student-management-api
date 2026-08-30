# Student Management System

A full-stack Student Management application built as an internship project. It provides a REST API (FastAPI + SQLAlchemy + MySQL) for managing student records, along with a simple web frontend (HTML/CSS/vanilla JavaScript) that consumes that API.

## Description

This project started as a basic FastAPI CRUD API for student records and was upgraded into a complete full-stack application with:
- A cleanly layered backend (routes / schemas / models / database logic separated)
- Input validation and meaningful error handling
- Search, filtering, and pagination
- A browser-based frontend for managing students without needing Swagger or Postman

## Features

- Create, view, update, and delete student records
- Search students by name, email, or course
- Filter students by course, department, or semester
- Paginated student listing
- Duplicate-email prevention on both create and update
- Field validation (age range, non-empty name/course, valid email/phone format)
- Dashboard showing total student count
- Responsive UI with loading, error, and success states
- Auto-generated API docs via Swagger UI

## Technology Stack

**Backend**
- Python 3
- FastAPI
- SQLAlchemy (ORM)
- MySQL
- PyMySQL (MySQL driver)
- Pydantic (validation)
- Uvicorn (ASGI server)
- python-dotenv (environment configuration)

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript (fetch API, no framework)

## Architecture

```
Frontend (HTML/CSS/JS)
        │  fetch()
        ▼
FastAPI REST API  (app/routers/students.py)
        │
        ▼
CRUD layer        (app/crud.py)
        │
        ▼
SQLAlchemy ORM     (app/models.py)
        │
        ▼
MySQL Database     (student_db)
```

**How a request flows through the system:**
1. The frontend calls an endpoint, e.g. `fetch('/students/')`.
2. FastAPI routes the request to the matching function in `app/routers/students.py`.
3. The router validates the request body against a Pydantic schema (`app/schemas.py`), then calls into `app/crud.py`.
4. `crud.py` uses a SQLAlchemy `Session` to build a query against the `Student` ORM model (`app/models.py`).
5. SQLAlchemy translates that into SQL and sends it to MySQL through the PyMySQL driver, using the connection configured in `app/database.py`.
6. The result flows back up: ORM objects → Pydantic response schema → JSON → the frontend.

**What each database piece does:**
- **`engine`** — knows how to talk to MySQL (host, credentials, driver). Created once at startup.
- **`SessionLocal`** — a factory for database sessions; each API request gets its own session via a FastAPI dependency (`get_db`), which is closed automatically when the request finishes.
- **`Base`** — the declarative base class that `Student` inherits from, letting SQLAlchemy map the Python class to the `students` table.

## Folder Structure

```
student-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app setup, CORS, static file serving
│   ├── database.py          # SQLAlchemy engine/session, reads .env
│   ├── models.py            # Student ORM model
│   ├── schemas.py           # Pydantic request/response schemas + validation
│   ├── crud.py               # All database query/write logic
│   └── routers/
│       └── students.py       # HTTP route handlers for /students
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env                       # Real credentials (NOT committed — see .gitignore)
├── .env.example                # Template for .env
├── .gitignore
├── requirements.txt
└── README.md
```

## MySQL Setup

1. Make sure MySQL Server is installed and running locally.
2. Create the database:
   ```sql
   CREATE DATABASE student_db;
   ```
   Tables are created automatically by SQLAlchemy the first time the app starts — no manual table creation needed.

## Environment Variable Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your real MySQL credentials:
   ```
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=student_db
   ```
3. `.env` is listed in `.gitignore` and will never be committed.

## Installation

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the Backend

```bash
uvicorn app.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

## Accessing the Frontend

Once the backend is running, open:

```
http://127.0.0.1:8000/
```

FastAPI serves the frontend directly — no separate server needed.

## Accessing Swagger (API Docs)

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint          | Description                                                                             |
|--------|--------------------|--------------------------------------------------------------------------------------------|
| POST   | `/students/`        | Create a new student                                                                      |
| GET    | `/students/`         | List students (supports `search`, `course`, `department`, `semester`, `skip`, `limit`)      |
| GET    | `/students/{id}`     | Get a single student by ID                                                                  |
| PUT    | `/students/{id}`     | Update a student                                                                              |
| DELETE | `/students/{id}`     | Delete a student                                                                                |

### Query parameters on `GET /students/`

| Parameter    | Type   | Description                                |
|--------------|--------|-----------------------------------------------|
| `search`     | string | Matches against name, email, or course           |
| `course`     | string | Filter by course (partial match)                    |
| `department` | string | Filter by department (partial match)                    |
| `semester`   | int    | Filter by exact semester                                    |
| `skip`       | int    | Number of records to skip (pagination)                        |
| `limit`      | int    | Max records to return, 1–100 (default 20)                        |

## Example Request / Response

**Request**
```http
POST /students/
Content-Type: application/json

{
  "name": "Alex Roy",
  "age": 20,
  "email": "alex@example.com",
  "phone": "9876543210",
  "course": "Computer Science",
  "department": "IT",
  "semester": 3
}
```

**Response — `201 Created`**
```json
{
  "id": 1,
  "name": "Alex Roy",
  "age": 20,
  "email": "alex@example.com",
  "phone": "9876543210",
  "course": "Computer Science",
  "department": "IT",
  "semester": 3
}
```

**Error example — duplicate email — `409 Conflict`**
```json
{
  "detail": "A student with this email already exists"
}
```

## Screenshots

_Add screenshots of the dashboard, student list, and add/edit form here before submission._

## Future Improvements

- Authentication (login for staff/admin)
- Bulk import/export (CSV)
- Sortable table columns
- Soft-delete / audit trail (`created_at`, `updated_at`)
- Automated test suite (pytest)
