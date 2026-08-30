from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=15, le=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    course: str = Field(..., min_length=1, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    semester: Optional[int] = Field(None, ge=1, le=12)

    @field_validator("name", "course")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty or whitespace")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value.strip() == "":
            return None
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.lstrip("+").isdigit():
            raise ValueError(
                "phone must contain only digits, spaces, hyphens, or a leading +"
            )
        return value


class StudentCreate(StudentBase):
    """Used for POST /students/"""
    pass


class StudentUpdate(StudentBase):
    """Used for PUT /students/{id}"""
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


class PaginatedStudents(BaseModel):
    """Response shape for GET /students/ with pagination metadata."""
    total: int
    skip: int
    limit: int
    items: list[StudentResponse]
