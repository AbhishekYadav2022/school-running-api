from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from app.schemas.other import session_schema
from app.models import model
from typing import List
from app.database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/sessions")


## Post Request API
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=session_schema.GetSession,
    tags=["sessions"],
)
def create_student(
    session: session_schema.CreateSession, db: Session = Depends(get_db)
):
    new_session = model.Session(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# Get All Sessions
@router.get("/", response_model=List[session_schema.GetSession], tags=["sessions"])
def get_all_sessions(
    db: Session = Depends(get_db),
    skip: int = 0,
    # name: Optional[str] = "",
    # std_class: Optional[str] = "",
    # phone: Optional[str] = "",
    limit: int = 20,
):
    all_sessions = (
        db.query(model.Session)
        # .filter(models.Session.name.contains(name))
        # .filter(models.Session.std_class == std_class)
        # .filter(models.Session.phone.contains(phone))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return all_sessions


# Get session by id
@router.get("/{id}", tags=["sessions"])
def get_session_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    session = db.query(model.Session).filter(model.Session.session_id == id).first()

    # If user not found
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {id} not found",
        )
    return session


# Delete session
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["sessions"])
def delete_session(
    id: int,
    db: Session = Depends(get_db),
):
    session = db.query(model.Session).filter(
        model.Session.session_id == id,
    )

    # Checking if the session exists
    if session.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No session found",
        )
    session.delete(synchronize_session=False)
    db.commit()


# Update Session
@router.put("/{id}", response_model=session_schema.GetSession, tags=["sessions"])
def update_session(
    id: int,
    updated_session: session_schema.CreateSession,
    db: Session = Depends(get_db),
):
    sess_query = db.query(model.Session).filter(model.Session.session_id == id)

    session = sess_query.first()

    # Raise Exception
    if session == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No session found",
        )
    sess_query.update(updated_session.dict(), synchronize_session=False)
    db.commit()
    return sess_query.first()
