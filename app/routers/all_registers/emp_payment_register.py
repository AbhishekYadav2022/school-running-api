from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from sqlalchemy import and_
from app.schemas.all_registers import emp_payment_register_schema
from app.models import model
from typing import List, Optional
from app.database import engine, get_db
from sqlalchemy.orm import Session
import datetime

model.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/emp_payments")


# <===================Get All Request====================>
@router.get(
    "/",
    # response_model=List[emp_payment_register_schema.PaymentData],
    tags=["registers"],
)
def get_all(
    db: Session = Depends(get_db),
    # skip: int = 0,
    session: Optional[str] = "",
    id: Optional[int] = "",
    name: Optional[str] = "",
    month: Optional[str] = "",
    # limit: int = 20,
):
    desired_columns = [
        model.Session.session_name.label("session"),
        model.Employee.emp_id.label("id"),
        model.Employee.first_name.label("name"),
        model.Month.month_name.label("month"),
        model.EmployeeSession.salary.label("salary"),
        model.EmployeePaymentRecord.is_full_paid.label("is_full_paid"),
        model.EmployeePaymentRecord.payment_amount.label("payment_amount"),
        model.EmployeePaymentRecord.created_at.label("last_payment_time"),
    ]

    all_payments = (
        db.query(*desired_columns)
        .select_from(model.SessionMonth)
        .join(
            model.EmployeeSession,
            model.SessionMonth.session_id == model.EmployeeSession.session_id,
        )
        .outerjoin(
            model.EmployeePaymentRecord,
            and_(
                model.SessionMonth.month_id == model.EmployeePaymentRecord.month_id,
                model.SessionMonth.session_id == model.EmployeePaymentRecord.session_id,
                model.EmployeeSession.emp_id == model.EmployeePaymentRecord.employee_id,
            ),
        )
        .join(
            model.Session,
            model.SessionMonth.session_id == model.Session.session_id,
        )
        .join(
            model.Employee,
            model.EmployeeSession.emp_id == model.Employee.emp_id,
        )
        .join(
            model.Month,
            model.SessionMonth.month_id == model.Month.month_id,
        )
        # .filter(model.Session.session_name(session))
        # .filter(model.Employee.emp_id == id)
        # .filter(model.Employee.first_name.contains(name))
        # .filter(model.Month.month_name.contains(month))
        # .offset(skip)
        # .limit(limit)
        .all()
    )

    structured_payments = []
    horizontal = []

    for payment in all_payments:
        payment_data = {
            "session": payment.session or "Unknown",
            "id": payment.id or 0,
            "name": payment.name or "Unknown",
            "month": payment.month or "Unknown",
            "salary": payment.salary or 0.0,
            "is_full_paid": payment.is_full_paid or False,
            "payment_amount": payment.payment_amount or 0,
            "last_payment_time": payment.last_payment_time
            or datetime.datetime(2000, 1, 1),
        }

        structured_payments.append(payment_data)

        # Testing
        dict = {"session": "", "id": "", "name": ""}
        dict["session"] = payment_data["session"]
        dict["id"] = payment_data["id"]
        dict["name"] = payment_data["name"]
        if payment_data["month"] is True:
            dict.update({f"{payment_data['month']}": True})

        horizontal.append(dict)
        # Testing

    print(horizontal)
    # return horizontal
    return structured_payments


# <========================Raw SQL=========================>
# select sessions.session_name          as session,
#        employees.emp_id               as id,
#        employees.first_name           as name,
#        months.month_name              as month,
#        salary,
#        is_full_paid,
#        payment_amount,
#        emp_payment_records.created_at as last_payment_time
# from session_months
#          join employee_session on session_months.session_id = employee_session.session_id
#          left join emp_payment_records on session_months.month_id = emp_payment_records.month_id and
#                                           session_months.session_id = emp_payment_records.session_id and
#                                           emp_payment_records.employee_id = employee_session.emp_id
#          join sessions on session_months.session_id = sessions.session_id
#          join employees on employee_session.emp_id = employees.emp_id
#          join months on session_months.month_id = months.month_id;
