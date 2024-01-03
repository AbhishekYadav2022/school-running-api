from fastapi import FastAPI, status, Depends, APIRouter, HTTPException, Request

from app.schemas.students import student_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/students")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=student_schema.GetStudent,
    tags=["students"],
)
def create_student(
    student: student_schema.CreateStudent, db: Session = Depends(get_db)
):
    new_student = model.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# <===================Get All Request====================>
@router.get("/", response_model=List[student_schema.GetStudent], tags=["students"])
def get_all_students(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_students = (
        db.query(model.Student)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_students


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["students"])
def get_student_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    student = db.query(model.Student).filter(model.Student.id == id).first()

    # If user not found
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found",
        )
    return student


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["students"])
def delete_student(
    id: int,
    db: Session = Depends(get_db),
):
    student = db.query(model.Student).filter(
        model.Student.id == id,
    )

    # Checking if the student exists
    if student.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found",
        )
    student.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=student_schema.GetStudent, tags=["students"])
def update_student(
    id: int,
    updated_student: student_schema.CreateStudent,
    db: Session = Depends(get_db),
):
    stud_query = db.query(model.Student).filter(model.Student.id == id)

    student = stud_query.first()

    # Raise Exception
    if student == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found",
        )
    stud_query.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return stud_query.first()
