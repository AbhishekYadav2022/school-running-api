from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import exam_details_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/exam_details")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=exam_details_schema.ExamDetails,
    tags=["exam_details"],
)
def create_exam_details(
    exam_details: exam_details_schema.ExamDetails, db: Session = Depends(get_db)
):
    new_exam_details = model.ExamDetails(**exam_details.dict())
    db.add(new_exam_details)
    db.commit()
    db.refresh(new_exam_details)
    return new_exam_details


# <===================Get All Request====================>
@router.get(
    "/", response_model=List[exam_details_schema.ExamDetails], tags=["exam_details"]
)
def get_all_exam_details(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_exam_details = (
        db.query(model.ExamDetails)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_exam_details
