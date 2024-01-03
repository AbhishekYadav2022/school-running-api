from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import Base
from sqlalchemy.orm import relationship


# <===================== Employees ===================>
class Department(Base):
    __tablename__ = "departments"
    dept_id = Column(Integer, primary_key=True, nullable=False)
    dept_name = Column(String(50), nullable=False)

    # Relationship with cascade deletion
    employee = relationship(
        "Employee", back_populates="departments", cascade="all, delete"
    )


class EmployeePaymentRecord(Base):
    __tablename__ = "emp_payment_records"
    employee_id = Column(
        Integer,
        ForeignKey("employees.emp_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    month_id = Column(
        Integer,
        ForeignKey("months.month_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    is_full_paid = Column(Boolean, default=True)
    payment_amount = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    dept_id = Column(
        Integer, ForeignKey("departments.dept_id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    employeeSession = relationship(
        "EmployeeSession", back_populates="employees", cascade="all, delete"
    )

    # relationship
    departments = relationship("Department", back_populates="employee")


class EmployeeSession(Base):
    __tablename__ = "employee_session"
    emp_id = Column(
        Integer,
        ForeignKey("employees.emp_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    salary = Column(Integer, nullable=False)

    # RELATIONSHIP
    employees = relationship("Employee", back_populates="employeeSession")

    sessions = relationship("Session", back_populates="employeeSession")


# <========================= Fees =========================>


class ClassDetails(Base):
    __tablename__ = "class_details"
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("std_classes.class_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    monthly_fees = Column(Integer, nullable=False)


class ExamDetails(Base):
    __tablename__ = "exam_details"
    exam_id = Column(
        Integer,
        ForeignKey("exams.exam_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("std_classes.class_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    exam_fees = Column(Integer, nullable=False)


class ExamFeesRecord(Base):
    __tablename__ = "exam_fees_record"
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    exam_id = Column(
        Integer,
        ForeignKey("exams.exam_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    is_full_paid = Column(Boolean, nullable=False)
    payment_amount = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Exam(Base):
    __tablename__ = "exams"
    exam_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    exam_name = Column(String(255), nullable=False, primary_key=True)


class OtherFeesDetails(Base):
    __tablename__ = "other_fees_details"
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    other_fees_id = Column(
        Integer,
        ForeignKey("other_fees.other_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("std_classes.class_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    fees_amount = Column(Integer, nullable=False)


class OtherFeesRecord(Base):
    __tablename__ = "other_fees_records"
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    other_fees_id = Column(
        Integer,
        ForeignKey("other_fees.other_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    is_full_paid = Column(Boolean, nullable=False)
    payment_amount = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class OtherFees(Base):
    __tablename__ = "other_fees"
    other_id = Column(Integer, primary_key=True, nullable=False)
    fees_name = Column(String, nullable=False)


class StudentFeesRecord(Base):
    __tablename__ = "student_fees_records"
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    month_id = Column(
        Integer,
        ForeignKey("months.month_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    is_full_paid = Column(Boolean, nullable=False)
    payment_amount = Column(Integer, nullable=False)
    last_payment_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# <======================== Other =======================>


class StdClass(Base):
    __tablename__ = "std_classes"
    class_id = Column(Integer, primary_key=True, nullable=False)
    class_name = Column(String, nullable=False)


class Guardian(Base):
    __tablename__ = "guardians"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # RELATIONSHIP
    students = relationship("Student", back_populates="guardian", cascade="all, delete")


class Month(Base):
    __tablename__ = "months"
    month_id = Column(Integer, primary_key=True, nullable=False)
    month_name = Column(String, nullable=False)


class SessionClass(Base):
    __tablename__ = "session_classes"
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("std_classes.class_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class SessionMonth(Base):
    __tablename__ = "session_months"
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    month_id = Column(
        Integer,
        ForeignKey("months.month_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, nullable=False)
    session_name = Column(String(7), nullable=False)

    # relationship
    employeeSession = relationship(
        "EmployeeSession", back_populates="sessions", cascade="all, delete"
    )


# <======================== Students =========================>


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    father_name = Column(String, nullable=False)
    mother_name = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    guardian_id = Column(
        Integer, ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # Relationship
    guardian = relationship(
        "Guardian",
        back_populates="students",
    )


class StudentClass(Base):
    __tablename__ = "student_classes"
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("std_classes.class_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
