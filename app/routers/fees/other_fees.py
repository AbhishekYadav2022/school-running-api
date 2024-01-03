from fastapi import FastAPI, status, Depends, APIRouter, HTTPException

from app.schemas.fees import other_fees_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/other_fees")


## <===================Post Request====================>
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=other_fees_schema.GetOtherFees,
    tags=["other_fees"],
)
def create_other_fees(
    other_fees: other_fees_schema.CreateOtherFees, db: Session = Depends(get_db)
):
    new_other_fees = model.OtherFees(**other_fees.dict())
    db.add(new_other_fees)
    db.commit()
    db.refresh(new_other_fees)
    return new_other_fees


# <===================Get All Request====================>
@router.get("/", response_model=List[other_fees_schema.GetOtherFees], tags=["other_fees"])
def get_all_other_fees(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_other_fees = (
        db.query(model.OtherFees)
        # .filter(models.Student.name.contains(name))
        # .filter(models.Student.std_class == std_class)
        # .filter(models.Student.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_other_fees


# <===================Get By ID Request====================>
@router.get("/{id}", tags=["other_fees"])
def get_other_fees_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    other_fees = db.query(model.OtherFees).filter(model.OtherFees.emp_id == id).first()

    # If user not found
    if not other_fees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OtherFees with id {id} not found",
        )
    return other_fees


# <===================Delete Request====================>
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["other_fees"])
def delete_other_fees(
    id: int,
    db: Session = Depends(get_db),
):
    other_fees = db.query(model.OtherFees).filter(
        model.OtherFees.emp_id == id,
    )

    # Checking if the other_fees exists
    if other_fees.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No other_fees found",
        )
    other_fees.delete(synchronize_session=False)
    db.commit()


# <===================Update Request====================>
@router.put("/{id}", response_model=other_fees_schema.GetOtherFees, tags=["other_fees"])
def update_other_fees(
    id: int,
    updated_other_fees: other_fees_schema.CreateOtherFees,
    db: Session = Depends(get_db),
):
    emp_query = db.query(model.OtherFees).filter(model.OtherFees.emp_id == id)

    other_fees = emp_query.first()

    # Raise Exception
    if other_fees == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No other_fees found",
        )
    emp_query.update(updated_other_fees.dict(), synchronize_session=False)
    db.commit()
    return emp_query.first()
