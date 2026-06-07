from sqlalchemy.orm import Session
from app.models import Student

def create_student(db: Session, student):
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


def get_students(db: Session):
    return db.query(Student).all()


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return student