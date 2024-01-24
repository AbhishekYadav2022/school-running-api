from fastapi import FastAPI
from .config import settings
from .routers.employees import (
    employee,
    department,
    employee_session,
    emp_payment_record,
)
from .routers.students import student, student_class
from .routers.other import (
    guardian,
    session,
    month,
    session_month,
    std_class,
    session_class,
)
from .routers.fees import (
    student_fees_record,
    exam,
    class_details,
    exam_fees_record,
    other_fees,
    other_fees_details,
    other_fees_record,
    exam_details,
)
from .routers.all_registers import emp_payment_register
from .database import engine
from .models import model

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {
        "message":"👋Hello, How are you?"
    }


app.include_router(employee.router)
app.include_router(department.router)
app.include_router(student.router)
app.include_router(guardian.router)
app.include_router(session.router)
app.include_router(employee_session.router)
app.include_router(month.router)
app.include_router(session_month.router)
app.include_router(student_fees_record.router)
app.include_router(std_class.router)
app.include_router(session_class.router)
app.include_router(exam.router)
app.include_router(class_details.router)
app.include_router(exam_fees_record.router)
app.include_router(other_fees.router)
app.include_router(other_fees_details.router)
app.include_router(other_fees_record.router)
app.include_router(student_class.router)
app.include_router(emp_payment_record.router)
app.include_router(exam_details.router)
app.include_router(emp_payment_register.router)
