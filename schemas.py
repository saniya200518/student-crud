from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator

class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @model_validator(mode="after")
    def need_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide email and/or phone")
        return self

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

class StudentOut(StudentCreate):
    id: int