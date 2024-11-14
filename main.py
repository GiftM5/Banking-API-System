from fastapi import FastAPI, Depends
from database.data import engine, Base,SessionLocal
from database.models.table import Account,Transaction
from pydantic import BaseModel
from sqlalchemy.orm import Session
# Create tables
class fetch_email(BaseModel):
    email: str
    name:str
    
Base.metadata.create_all(bind=engine)

session = SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# def database(db: SessionLocal = Depends(get_db)):
#     email = Session.query(Account).all()
#     print(email)
    
# database(Account.email)