from pydantic import BaseModel

class ClassDetails(BaseModel):
    session_id: int
    class_id: int
    monthly_fees: int

    class Config:
        from_attributes = True