# main.py
from fastapi import FastAPI
from .database import Engine, Base
from .database.models.data import Account
from .database.models.transaction import Transaction

# Create tables
Base.metadata.create_all(bind=Engine)

app = FastAPI()
