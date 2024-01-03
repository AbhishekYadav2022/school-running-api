from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.employees import employee_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/employees")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=employee_schema.GetEmployee,
    tags=["employees"],
)
def create_employee(
    employee: employee_schema.CreateEmployee, db: Session = Depends(get_db)
):
    new_employee = model.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# <===================Get All Request====================>
@router.get("/", response_model=List[employee_schema.GetEmployee], tags=["employees"])
def get_all_employees(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_employees = (
        db.query(model.Employee)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_employees


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["employees"])
def get_employee_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    employee = db.query(model.Employee).filter(model.Employee.emp_id == id).first()

    # If user not found
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found",
        )
    return employee


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["employees"])
def delete_employee(
    id: int,
    db: Session = Depends(get_db),
):
    employee = db.query(model.Employee).filter(
        model.Employee.emp_id == id,
    )

    # Checking if the employee exists
    if employee.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employee found",
        )
    employee.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=employee_schema.GetEmployee, tags=["employees"])
def update_employee(
    id: int,
    updated_employee: employee_schema.CreateEmployee,
    db: Session = Depends(get_db),
):
    emp_query = db.query(model.Employee).filter(model.Employee.emp_id == id)

    employee = emp_query.first()

    # Raise Exception
    if employee == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employee found",
        )
    emp_query.update(updated_employee.dict(), synchronize_session=False)
    db.commit()
    return emp_query.first()
