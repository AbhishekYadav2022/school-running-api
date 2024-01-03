from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.other import class_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/std_classes")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=class_schema.GetClass,
    tags=["std_classes"],
)
def create_std_class(
    std_class: class_schema.CreateClass, db: Session = Depends(get_db)
):
    new_std_class = model.StdClass(**std_class.dict())
    db.add(new_std_class)
    db.commit()
    db.refresh(new_std_class)
    return new_std_class


# <===================Get All Request====================>
@router.get("/", response_model=List[class_schema.GetClass], tags=["std_classes"])
def get_all_std_classes(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_std_classes = (
        db.query(model.StdClass)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_std_classes


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["std_classes"])
def get_std_class_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    std_class = db.query(model.StdClass).filter(model.StdClass.class_id == id).first()

    # If user not found
    if not std_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"StdClass with id {id} not found",
        )
    return std_class


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["std_classes"])
def delete_std_class(
    id: int,
    db: Session = Depends(get_db),
):
    std_class = db.query(model.StdClass).filter(
        model.StdClass.class_id == id,
    )

    # Checking if the std_class exists
    if std_class.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No std_class found",
        )
    std_class.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=class_schema.GetClass, tags=["std_classes"])
def update_std_class(
    id: int,
    updated_std_class: class_schema.CreateClass,
    db: Session = Depends(get_db),
):
    emp_query = db.query(model.StdClass).filter(model.StdClass.class_id == id)

    std_class = emp_query.first()

    # Raise Exception
    if std_class == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No std_class found",
        )
    emp_query.update(updated_std_class.dict(), synchronize_session=False)
    db.commit()
    return emp_query.first()
