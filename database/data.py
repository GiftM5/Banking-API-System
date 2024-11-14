from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "sqlite:///data.db"

# Creating the SQLAlchemy engine
engine = create_engine(
    database_url, connect_args={"check_same_thread": False}  # Required for SQLite
)

# SessionLocal is used for creating a session per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating models
Base = declarative_base()