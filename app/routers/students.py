from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import PaginatedStudents, StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student_by_email(db, student.email):
        raise HTTPException(
            status_code=409, detail="A student with this email already exists"
        )

    try:
        return crud.create_student(db, student)
    except IntegrityError:
        # Safety net for a race condition between the check above and the
        # insert (e.g. two requests at the same time). Never leak raw DB
        # error details to the client.
        db.rollback()
        raise HTTPException(
            status_code=409, detail="A student with this email already exists"
        )


@router.get("/", response_model=PaginatedStudents)
def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    search: Optional[str] = Query(
        None, description="Search by name, email, or course"
    ),
    course: Optional[str] = Query(None, description="Filter by course"),
    department: Optional[str] = Query(None, description="Filter by department"),
    semester: Optional[int] = Query(None, description="Filter by semester"),
    db: Session = Depends(get_db),
):
    """
    Acts as both the student list AND the search/filter endpoint:
    GET /students/?search=alex
    GET /students/?course=CS&department=IT&semester=3
    GET /students/?skip=20&limit=20   (pagination)
    """
    total, items = crud.get_students(
        db,
        skip=skip,
        limit=limit,
        search=search,
        course=course,
        department=department,
        semester=semester,
    )
    return PaginatedStudents(total=total, skip=skip, limit=limit, items=items)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentUpdate, db: Session = Depends(get_db)
):
    if crud.get_student_by_email(db, student.email, exclude_id=student_id):
        raise HTTPException(
            status_code=409, detail="Another student already uses this email"
        )

    try:
        updated = crud.update_student(db, student_id, student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Another student already uses this email"
        )

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": f"Student with ID {student_id} deleted successfully"}
