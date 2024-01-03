from pydantic import BaseModel
from datetime import datetime

# Schema For Creating Student
class CreateStudentFeesRecord(BaseModel):
    student_id: int
    session_id: int
    month_id: int
    is_full_paid: bool
    payment_amount: str

class GetStudentFeesRecord(BaseModel):
    student_id: int
    session_id: int
    month_id: int
    is_full_paid: bool
    payment_amount: str
    last_payment_time: datetime

    class Config:
        from_attributes = True