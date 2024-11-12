from fastapi import FastAPI
from database.data import engine, Base
from database.models.table import Account,Transaction


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
