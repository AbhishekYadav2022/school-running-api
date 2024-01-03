from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.students import student_class_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/student_classes")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=student_class_schema.StudentClass,
    tags=["student_classes"],
)
def create_student_class(
    student_class: student_class_schema.StudentClass, db: Session = Depends(get_db)
):
    new_student_class = model.StudentClass(**student_class.dict())
    db.add(new_student_class)
    db.commit()
    db.refresh(new_student_class)
    return new_student_class


# <===================Get All Request====================>
@router.get("/", response_model=List[student_class_schema.StudentClass], tags=["student_classes"])
def get_all_student_classes(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_student_classes = (
        db.query(model.StudentClass)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_student_classes

