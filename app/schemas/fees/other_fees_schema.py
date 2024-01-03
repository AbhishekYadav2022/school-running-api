from pydantic import BaseModel

class CreateOtherFees(BaseModel):
    other_id: int
    fees_name: str

class GetOtherFees(BaseModel):
    fees_name: str

    class Config:
        from_attributes = True
