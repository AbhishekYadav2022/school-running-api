from fastapi import FastAPI
from .routers import student
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my api!"}

app.include_router(student.router)