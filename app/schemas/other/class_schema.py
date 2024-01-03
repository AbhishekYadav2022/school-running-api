from pydantic import BaseModel

# Schema For Creating Student
class CreateClass(BaseModel):
    class_name: str

class GetClass(BaseModel):
    class_id: int
    class_name: str

    class Config:
        from_attributes = True