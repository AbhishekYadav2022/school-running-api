from pydantic import BaseModel

class ExamDetails(BaseModel):
    exam_id: str
    session_id: int
    class_id: int
    exam_fees: int

    class Config:
        from_attributes = True