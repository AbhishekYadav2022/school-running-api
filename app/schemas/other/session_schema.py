from pydantic import BaseModel

# Schema For Creating Student
class CreateSession(BaseModel):
    session_name: str

class GetSession(BaseModel):
    session_id: int
    session_name: str

    class Config:
        from_attributes = True