from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import exam_fees_record_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/exam_fees_records")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=exam_fees_record_schema.ExamFeesRecord,
    tags=["exam_fees_records"],
)
def create_exam_fees_record(
    exam_fees_record: exam_fees_record_schema.ExamFeesRecord, db: Session = Depends(get_db)
):
    new_exam_fees_record = model.ExamFeesRecord(**exam_fees_record.dict())
    db.add(new_exam_fees_record)
    db.commit()
    db.refresh(new_exam_fees_record)
    return new_exam_fees_record


# <===================Get All Request====================>
@router.get("/", response_model=List[exam_fees_record_schema.ExamFeesRecord], tags=["exam_fees_records"])
def get_all_exam_fees_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_exam_fees_records = (
        db.query(model.ExamFeesRecord)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_exam_fees_records
