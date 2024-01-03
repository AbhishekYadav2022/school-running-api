from pydantic import BaseModel

# Schema For Creating Student
class CreateMonth(BaseModel):
    month_name: str

class GetMonth(BaseModel):
    month_id: int
    month_name: str

    class Config:
        from_attributes = True