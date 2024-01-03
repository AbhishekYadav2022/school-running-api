from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.employees import department_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/departments")


## Post Request API
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=department_schema.GetDepartment,
    tags=["departments"],
)
def create_department(
    deparment: department_schema.CreateDepartment, db: Session = Depends(get_db)
):
    new_department = model.Department(**deparment.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


# Get All Departments
@router.get(
    "/", response_model=List[department_schema.GetDepartment], tags=["departments"]
)
def get_all_departments(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_departments = (
        db.query(model.Department)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_departments


# Get department by id
@router.get("/{id}", tags=["departments"])
def get_department_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    department = (
        db.query(model.Department).filter(model.Department.dept_id == id).first()
    )

    # If user not found
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {id} not found",
        )
    return department


# Delete department
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["departments"])
def delete_department(
    id: int,
    db: Session = Depends(get_db),
):
    department = db.query(model.Department).filter(
        model.Department.dept_id == id,
    )

    # Checking if the department exists
    if department.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No department found",
        )
    department.delete(synchronize_session=False)
    db.commit()


# Update Department
@router.put(
    "/{id}", response_model=department_schema.GetDepartment, tags=["departments"]
)
def update_department(
    id: int,
    updated_department: department_schema.CreateDepartment,
    db: Session = Depends(get_db),
):
    dpt_query = db.query(model.Department).filter(model.Department.dept_id == id)

    department = dpt_query.first()

    # Raise Exception
    if department == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No department found",
        )
    dpt_query.update(updated_department.dict(), synchronize_session=False)
    db.commit()
    return dpt_query.first()
