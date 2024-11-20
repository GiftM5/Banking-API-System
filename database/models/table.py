from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date,Enum
from ..data import Base
from sqlalchemy.orm import relationship
from datetime import date
import uuid


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(
        Integer,
        default=lambda: int(str(uuid.uuid4().int)[:10]),  
        # The line 14 is generates a unique 10-digit number each time a new record is created.
        unique=True,
        nullable=False
    )
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    creation_date=Column(Date,default=date.today)

    transactions = relationship("Transaction", back_populates="account")
    
    
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.account_number'))
    amount = Column(Float, nullable=False)
    type = Column(Enum('deposit', 'withdrawal', name='transaction_type'), nullable=False)

    account = relationship("Account", back_populates="transactions")
    
    
def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.balance <= 0:
            raise ValueError("Balance must be greater than 0")