from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.other import session_class_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/session_classes")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=session_class_schema.GetSessionClass,
    tags=["session_classes"],
)
def create_session_class(
    session_class: session_class_schema.CreateSessionClass, db: Session = Depends(get_db)
):
    new_session_class = model.SessionClass(**session_class.dict())
    db.add(new_session_class)
    db.commit()
    db.refresh(new_session_class)
    return new_session_class


# <===================Get All Request====================>
@router.get("/", response_model=List[session_class_schema.GetSessionClass], tags=["session_classes"])
def get_all_session_classes(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_session_classes = (
        db.query(model.SessionClass)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_session_classes