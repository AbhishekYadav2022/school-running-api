from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import class_details_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/class_details")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=class_details_schema.ClassDetails,
    tags=["class_details"],
)
def create_class_details(
    class_details: class_details_schema.ClassDetails, db: Session = Depends(get_db)
):
    new_class_details = model.ClassDetails(**class_details.dict())
    db.add(new_class_details)
    db.commit()
    db.refresh(new_class_details)
    return new_class_details


# <===================Get All Request====================>
@router.get(
    "/", response_model=List[class_details_schema.ClassDetails], tags=["class_details"]
)
def get_all_class_details(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_class_details = (
        db.query(model.ClassDetails)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_class_details
