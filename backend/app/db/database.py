from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
SQLALCHEMY_DATABASE_URL = 'postgresql://stud_user:student@localhost:5432/stud_assistant'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
         db.close()


def create_database():

    """
    Run this only when creating the database!!!
    """
    Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        # create a session
        db: Session = SessionLocal()
        # run a simple query (count users)
        result = db.execute(text("CREATE TABLE temp(name VARCHAR(255));"))
        print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)
    finally:
        db.close()
if __name__ == '__main__':
    create_database()
