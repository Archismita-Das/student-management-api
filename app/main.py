from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import Student
from app.schemas import StudentCreate, StudentResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Record Management API"
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Create Student API (POST)
# -------------------------
@app.post("/students/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = Student(
        name=student.name,
        age=student.age,
        email=student.email,
        course=student.course
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


# -------------------------
# View All Students API (GET)
# -------------------------
@app.get("/students/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Student).all()


# -------------------------
# View Single Student API
# Dynamic Routing Example
# -------------------------
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# -------------------------
# Update Student API (PUT)
# Final Enhancement
# -------------------------
@app.put("/students/{student_id}",
         response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.email = student.email
    existing_student.course = student.course

    db.commit()
    db.refresh(existing_student)

    return existing_student


# -------------------------
# Delete Student API
# -------------------------
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": f"Student with ID {student_id} deleted successfully"
    }


# -------------------------
# Home Route
# -------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to Student Record Management API"
    }