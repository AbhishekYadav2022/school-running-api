from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from app.schemas.other import guardian_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/guardians")


## Post Request API
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=guardian_schema.GetGuardian,
    tags=["guardians"],
)
def create_student(
    guardian: guardian_schema.CreateGuardian, db: Session = Depends(get_db)
):
    new_guardian = model.Guardian(**guardian.dict())
    db.add(new_guardian)
    db.commit()
    db.refresh(new_guardian)
    return new_guardian


# Get All Students
@router.get("/", response_model=List[guardian_schema.GetGuardian], tags=["guardians"])
def get_all_guardians(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_guardians = (
        db.query(model.Guardian)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_guardians


# Get guardian by id
@router.get("/{id}", tags=["guardians"])
def get_guardian_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    guardian = db.query(model.Guardian).filter(model.Guardian.id == id).first()

    # If user not found
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guardian with id {id} not found",
        )
    return guardian


# Delete guardian
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["guardians"])
def delete_guardian(
    id: int,
    db: Session = Depends(get_db),
):
    guardian = db.query(model.Guardian).filter(
        model.Guardian.id == id,
    )

    # Checking if the guardian exists
    if guardian.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No guardian found",
        )
    guardian.delete(synchronize_session=False)
    db.commit()


# Update Guardian
@router.put("/{id}", response_model=guardian_schema.GetGuardian, tags=["guardians"])
def update_guardian(
    id: int,
    updated_guardian: guardian_schema.CreateGuardian,
    db: Session = Depends(get_db),
):
    dpt_query = db.query(model.Guardian).filter(model.Guardian.id == id)

    guardian = dpt_query.first()

    # Raise Exception
    if guardian == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No guardian found",
        )
    dpt_query.update(updated_guardian.dict(), synchronize_session=False)
    db.commit()
    return dpt_query.first()
