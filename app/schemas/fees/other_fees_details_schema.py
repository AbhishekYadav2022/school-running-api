from pydantic import BaseModel

# Schema For Creating Student
class OtherFeesDetails(BaseModel):
    session_id: int
    class_id: int
    fees_amount: int

    class Config:
        from_attributes = True