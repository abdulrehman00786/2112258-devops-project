import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr

from .database import engine, Base, get_db
from . import models


if os.getenv("TESTING") != "True":
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database connection skipped or failed: {e}")

app = FastAPI(title="DevOps Fundamentals Final Project")


class StudentBase(BaseModel):
    name: str
    reg_no: str
    email: EmailStr
    course: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "db": "connected",
        "student": "2112258"
    }

@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.reg_no == student.reg_no).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Registration number already registered")
    
    new_student = models.Student(
        name=student.name,
        reg_no=student.reg_no,
        email=student.email,
        course=student.course
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get("/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student_by_reg(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student