from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.employees import employee_session_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/employee_sessions")


## Post Request
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=employee_session_schema.EmployeeSession,
    tags=["employee_sessions"],
)
def create_employee_session(
    employee_session: employee_session_schema.EmployeeSession,
    db: Session = Depends(get_db),
):
    new_employee_session = model.EmployeeSession(**employee_session.dict())
    db.add(new_employee_session)
    db.commit()
    db.refresh(new_employee_session)
    return new_employee_session


# Get Request
@router.get(
    "/",
    response_model=List[employee_session_schema.EmployeeSession],
    tags=["employee_sessions"],
)
def get_all_employee_sessions(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_employee_sessions = (
        db.query(model.EmployeeSession)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_employee_sessions
