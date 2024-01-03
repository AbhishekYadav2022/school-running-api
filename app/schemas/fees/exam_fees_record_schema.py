from pydantic import BaseModel

class ExamFeesRecord(BaseModel):
    student_id: int
    session_id: int
    exam_name: str
    is_full_paid: bool
    payment_amount: int
    
    class Config:
        from_attributes = True