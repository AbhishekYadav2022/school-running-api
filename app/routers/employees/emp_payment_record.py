from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.employees import emp_payment_record_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/emp_payment_records")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=emp_payment_record_schema.EmpPaymentRecord,
    tags=["emp_payment_records"],
)
def create_emp_payment_record(
    emp_payment_record: emp_payment_record_schema.EmpPaymentRecord,
    db: Session = Depends(get_db),
):
    new_emp_payment_record = model.EmployeePaymentRecord(**emp_payment_record.dict())
    db.add(new_emp_payment_record)
    db.commit()
    db.refresh(new_emp_payment_record)
    return new_emp_payment_record


# <===================Get All Request====================>
@router.get(
    "/",
    response_model=List[emp_payment_record_schema.EmpPaymentRecord],
    tags=["emp_payment_records"],
)
def get_all_emp_payment_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_emp_payment_records = (
        db.query(model.EmployeePaymentRecord)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_emp_payment_records
