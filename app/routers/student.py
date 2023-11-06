from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from typing import List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional

models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/students")


## Post Request API
@router.post(
    "/new", status_code=status.HTTP_201_CREATED, response_model=schemas.GetStudent
)
def create_student(student: schemas.CreateStudent, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# Get All Students
@router.get("/", response_model=List[schemas.GetStudent])
def get_all_students(
    db: Session = Depends(get_db),
    skip: int = 0,
    name: Optional[str] = "",
    std_class: Optional[str] = "",
    phone: Optional[str] = "",
    limit: int = 20,
):
    students = (
        db.query(models.Student)
        .filter(models.Student.name.contains(name))
        .filter(models.Student.std_class.contains(std_class))
        .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return students


# Get student by id
@router.get(
    "/{id}",
)
def get_student_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    student = db.query(models.Student).filter(models.Student.id == id).first()

    # If user not found
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found",
        )
    return student


# Delete student
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    id: int,
    db: Session = Depends(get_db),
):
    student = db.query(models.Student).filter(
        models.Student.id == id,
    )

    # Checking if the student exists
    if student.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found",
        )
    student.delete(synchronize_session=False)
    db.commit()


# Update student
@router.put("/{id}", response_model=schemas.GetStudent)
def update_student(
    id: int, updated_student: schemas.CreateStudent, db: Session = Depends(get_db)
):
    std_query = db.query(models.Student).filter(models.Student.id == id)

    student = std_query.first()

    # Raise Exception
    if student == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found",
        )
    std_query.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return std_query.first()
