from sqlalchemy import Column, Integer, String
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    reg_no = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    course = Column(String)