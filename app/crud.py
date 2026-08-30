from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(
    db: Session, email: str, exclude_id: Optional[int] = None
) -> Optional[Student]:
    """
    Look up a student by email. When exclude_id is given (used during
    updates), a student matching that id is not counted as a collision.
    """
    query = db.query(Student).filter(Student.email == email)
    if exclude_id is not None:
        query = query.filter(Student.id != exclude_id)
    return query.first()


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    course: Optional[str] = None,
    department: Optional[str] = None,
    semester: Optional[int] = None,
) -> tuple[int, list[Student]]:
    """
    Returns (total_matching_count, page_of_students).
    `search` matches against name, email, or course.
    `course` / `department` / `semester` are exact/partial filters.
    """
    query = db.query(Student)

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.ilike(like),
                Student.email.ilike(like),
                Student.course.ilike(like),
            )
        )

    if course:
        query = query.filter(Student.course.ilike(f"%{course}%"))

    if department:
        query = query.filter(Student.department.ilike(f"%{department}%"))

    if semester is not None:
        query = query.filter(Student.semester == semester)

    total = query.count()
    items = query.order_by(Student.id).offset(skip).limit(limit).all()

    return total, items


def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(
    db: Session, student_id: int, student: StudentUpdate
) -> Optional[Student]:
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    for field, value in student.model_dump().items():
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> Optional[Student]:
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    db.delete(db_student)
    db.commit()
    return db_student
