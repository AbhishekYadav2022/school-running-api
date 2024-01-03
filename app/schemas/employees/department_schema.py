from pydantic import BaseModel

class CreateDepartment(BaseModel):
    dept_name: str

class GetDepartment(BaseModel):
    dept_id: int
    dept_name: str

    class Config:
        from_attributes = True