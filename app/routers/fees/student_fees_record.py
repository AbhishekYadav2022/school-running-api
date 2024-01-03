from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import student_fees_record_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/student_fees_records")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=student_fees_record_schema.GetStudentFeesRecord,
    tags=["student_fees_records"],
)
def create_student_fees_record(
    student_fees_record: student_fees_record_schema.CreateStudentFeesRecord,
    db: Session = Depends(get_db),
):
    new_student_fees_record = model.StudentFeesRecord(**student_fees_record.dict())
    db.add(new_student_fees_record)
    db.commit()
    db.refresh(new_student_fees_record)
    return new_student_fees_record


# <===================Get All Request====================>
@router.get(
    "/",
    response_model=List[student_fees_record_schema.GetStudentFeesRecord],
    tags=["student_fees_records"],
)
def get_all_student_fees_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_student_fees_records = (
        db.query(model.StudentFeesRecord)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_student_fees_records
