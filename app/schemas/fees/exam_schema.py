from pydantic import BaseModel


class CreateExam(BaseModel):
    exam_name: str

class GetExam(BaseModel):
    exam_id: int
    exam_name: str

    class Config:
        from_attributes = True
