from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database.data import get_db
from database.models.table import Account,Transaction

account_router = APIRouter(tags=["Accounts"])

#pydantic models for creating account
class create_account_base(BaseModel):
    email: EmailStr
    name:str
    surname:str
    
    
#endpoint for creating account
@account_router.post('/account/create/')
async def create_account(account:create_account_base, db:Session=Depends(get_db), response_model=create_account_base):
    email_match=db.query(Account).filter(Account.email==account.email).first()
    if email_match:
        return {
            'message':'Account with this email already exist'
            }
    else:
        new_acc=Account(email=account.email,name=account.name,surname=account.surname)
        db.add(new_acc)
        db.commit()
        db.refresh
        return{
            "message": 'account created','email':account.email
            }
    
#endpoint for retriving spacific user data with id parameter
@account_router.get('/account/{account_id}')
async def fetch_account(account_id:int=Path(description="Account ID"), db:Session=Depends(get_db),response_model=create_account_base):
    _account=db.query(Account).filter(Account.id==account_id).first()
    if _account:
        return {
            'account_Number': _account.account_number, 
            'email': _account.email, 
            'name': _account.name,
            'surname':_account.surname, 
            'balance': _account.balance,
            'account_created':_account.creation_date}
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
#endpoint for updating information
@account_router.put('/account/{account_id}')
async def update_account(account_id:int = Path(description= "Updating Account ID"),account:create_account_base = Depends(),db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()

    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    existing_account.email  = account.email
    existing_account.name = account.name
    existing_account.surname = account.surname

    db.commit()
    db.refresh(existing_account)

    return {
            'account Number': existing_account.id, 
            'email': existing_account.email, 
            'name':existing_account.name,
            'surname':existing_account.surname}

#endpoint for deleting an account
@account_router.delete('/account/{account_id}')
async def update_account(account_id:int = Path(description= "Delete Account ID"),account:create_account_base = Depends(),db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()

    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(existing_account)
    db.commit()

    return(f"Account_id{account_id} has been deleted successfully")

