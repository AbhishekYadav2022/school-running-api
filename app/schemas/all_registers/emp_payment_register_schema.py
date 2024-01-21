from pydantic import BaseModel
from datetime import datetime


class PaymentData(BaseModel):
    session: str
    id: int
    name: str
    month: str
    salary: int
    is_full_paid: bool
    payment_amount: int
    last_payment_time: datetime

    class Config:
        from_attributes = True
