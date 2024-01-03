from pydantic import BaseModel

class EmployeeSession(BaseModel):
    emp_id: int
    session_id: int
    salary: int

    class Config:
        from_attributes = True