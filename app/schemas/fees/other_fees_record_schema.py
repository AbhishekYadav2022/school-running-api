from pydantic import BaseModel

class OtherFeesRecord(BaseModel):
    student_id: int
    session_id: int
    fees_name: str
    is_full_paid: int
    payment_amount: int

    class Config:
        from_attributes = True