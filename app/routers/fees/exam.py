from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import exam_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/exams")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=exam_schema.GetExam,
    tags=["exams"],
)
def create_exam(
    exam: exam_schema.CreateExam, db: Session = Depends(get_db)
):
    new_exam = model.Exam(**exam.dict())
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam


# <===================Get All Request====================>
@router.get("/", response_model=List[exam_schema.GetExam], tags=["exams"])
def get_all_exams(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_exams = (
        db.query(model.Exam)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_exams


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["exams"])
def get_exam_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    exam = db.query(model.Exam).filter(model.Exam.exam_id == id).first()

    # If user not found
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {id} not found",
        )
    return exam


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["exams"])
def delete_exam(
    id: int,
    db: Session = Depends(get_db),
):
    exam = db.query(model.Exam).filter(
        model.Exam.exam_id == id,
    )

    # Checking if the exam exists
    if exam.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exam found",
        )
    exam.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=exam_schema.GetExam, tags=["exams"])
def update_exam(
    id: int,
    updated_exam: exam_schema.CreateExam,
    db: Session = Depends(get_db),
):
    exam_query = db.query(model.Exam).filter(model.Exam.exam_id == id)

    exam = exam_query.first()

    # Raise Exception
    if exam == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exam found",
        )
    exam_query.update(updated_exam.dict(), synchronize_session=False)
    db.commit()
    return exam_query.first()
