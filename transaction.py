from fastapi import APIRouter, HTTPException, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from database.data import get_db
from database.models.table import Account,Transaction

transactions_router = APIRouter(tags=["Transactions"])

#pydantic model for transactions
class transaction_actions(BaseModel):
    email: EmailStr
    name:str
    surname: str
    amount: float= Field(gt=0,description="Amount must be positive")
    
#endpoint for adding funds to account
@transactions_router.post('/account/{account_id}/deposit/')
async def deposit(account_id:int = Path(description= "Account ID to deposit funds"), account_data : transaction_actions = Depends(),db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.balance += account_data.amount
    
    db.commit()
    db.refresh(account)

    return {
        "message": f"Successfully deposited {account_data.amount} to account {account_id}.",
        "new_balance": account.balance
    }

#endpoint for withdrawing fund from account
@transactions_router.post('/account/{account_id}/withdraw')
async def withdraw_funds(account_id: int = Path(description="Account ID to withdraw funs"), account_data: transaction_actions = Depends(),db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.balance < account_data.amount:
        raise HTTPException(status_code=404, detail="Insufficient funds")

    account.balance -= account_data.amount
    
    db.commit()
    db.refresh(account)

    return {
        "message": f"Successfully withdraw {account_data.amount} from account {account_id}.",
        "new_balance": account.balance
    }
    
