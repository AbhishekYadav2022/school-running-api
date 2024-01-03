from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.other import month_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/months")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=month_schema.GetMonth,
    tags=["months"],
)
def create_month(month: month_schema.CreateMonth, db: Session = Depends(get_db)):
    new_month = model.Month(**month.dict())
    db.add(new_month)
    db.commit()
    db.refresh(new_month)
    return new_month


# <===================Get All Request====================>
@router.get("/", response_model=List[month_schema.GetMonth], tags=["months"])
def get_all_months(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_months = (
        db.query(model.Month)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_months


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["months"])
def get_month_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    month = db.query(model.Month).filter(model.Month.month_id == id).first()

    # If user not found
    if not month:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Month with id {id} not found",
        )
    return month


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["months"])
def delete_month(
    id: int,
    db: Session = Depends(get_db),
):
    month = db.query(model.Month).filter(
        model.Month.month_id == id,
    )

    # Checking if the month exists
    if month.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No month found",
        )
    month.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=month_schema.GetMonth, tags=["months"])
def update_month(
    id: int,
    updated_month: month_schema.CreateMonth,
    db: Session = Depends(get_db),
):
    month_query = db.query(model.Month).filter(model.Month.month_id == id)

    month = month_query.first()

    # Raise Exception
    if month == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No month found",
        )
    month_query.update(updated_month.dict(), synchronize_session=False)
    db.commit()
    return month_query.first()
