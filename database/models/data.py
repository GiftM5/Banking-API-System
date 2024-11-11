from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)

    transactions = relationship("Transaction", back_populates="account")
    
    
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # 'deposit' or 'withdrawal'

    account = relationship("Account", back_populates="transactions")