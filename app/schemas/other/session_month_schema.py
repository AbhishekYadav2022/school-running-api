from pydantic import BaseModel


# Schema For Creating Student
class CreateSessionMonth(BaseModel):
    session_id: int
    month_id: int

class GetSessionMonth(BaseModel):
    session_id: int
    month_id: int

    class Config:
        from_attributes = True