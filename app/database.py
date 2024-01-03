from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creating Connection With Database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/new_school_database"

# SQLALCHEMY_DATABASE_URL = "postgresql://abhishek:0CYu5vJKdK7kAaqVPcRdX4OTkwzlzbg9@dpg-cl3f1u9novjs73bh09tg-a.singapore-postgres.render.com/studentdb_mb8e"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
