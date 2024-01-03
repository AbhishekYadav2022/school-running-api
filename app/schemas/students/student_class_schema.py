from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StudentClass(BaseModel):
    student_id: int
    session_id: int
    class_id: int

    class Config:
        from_attributes = True