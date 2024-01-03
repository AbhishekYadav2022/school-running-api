from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.other import session_month_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/session_months")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=session_month_schema.GetSessionMonth,
    tags=["session_months"],
)
def create_session_month(
    session_month: session_month_schema.CreateSessionMonth, db: Session = Depends(get_db)
):
    new_session_month = model.SessionMonth(**session_month.dict())
    db.add(new_session_month)
    db.commit()
    db.refresh(new_session_month)
    return new_session_month


# <===================Get All Request====================>
@router.get("/", response_model=List[session_month_schema.GetSessionMonth], tags=["session_months"])
def get_all_session_months(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_session_months = (
        db.query(model.SessionMonth)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_session_months
