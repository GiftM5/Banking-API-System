from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Creating the SQLAlchemy engine
Engine = create_engine(
    database_url, connect_args={"check_same_thread": False}  # Required for SQLite
)

# SessionLocal is used for creating a session per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating models
Base = declarative_base()