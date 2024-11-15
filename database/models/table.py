from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date
from ..data import Base
from sqlalchemy.orm import relationship
from datetime import date
import uuid
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_number=Column(Integer,default=int(uuid.uuid4().int % 1e10),unique=True,nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    creation_date=Column(Date,default=date.today)

    transactions = relationship("Transaction", back_populates="account")
    
    
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # 'deposit' or 'withdrawal'

    account = relationship("Account", back_populates="transactions")