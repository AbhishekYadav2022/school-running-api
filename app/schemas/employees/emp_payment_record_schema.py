from pydantic import BaseModel

class EmpPaymentRecord(BaseModel):
    employee_id: int
    session_id: int
    month_id: int
    is_full_paid: bool
    payment_amount: int

    class Config:
        from_attributes = True