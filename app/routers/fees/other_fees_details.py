from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import other_fees_details_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/other_fees_details")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=other_fees_details_schema.OtherFeesDetails,
    tags=["other_fees_details"],
)
def create_other_fees_details(
    other_fees_details: other_fees_details_schema.OtherFeesDetails, db: Session = Depends(get_db)
):
    new_other_fees_details = model.OtherFeesDetails(**other_fees_details.dict())
    db.add(new_other_fees_details)
    db.commit()
    db.refresh(new_other_fees_details)
    return new_other_fees_details


# <===================Get All Request====================>
@router.get("/", response_model=List[other_fees_details_schema.OtherFeesDetails], tags=["other_fees_details"])
def get_all_other_fees_details(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_other_fees_details = (
        db.query(model.OtherFeesDetails)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_other_fees_details

