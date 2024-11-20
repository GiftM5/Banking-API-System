from fastapi import FastAPI, Depends,Path,HTTPException
from database.data import engine, Base,SessionLocal
from database.models.table import Account,Transaction
from pydantic import BaseModel, EmailStr,Field 
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#pydantic models for creating account
class create_account_base(BaseModel):
    email: EmailStr
    name:str
    surname:str
    balance: float= Field(gt=0,description="Balance must be positive")
#pydantic model for retrieving data

#pydantic model for transactions
class transaction_actions(BaseModel):
    email: EmailStr
    name:str
    surname: str
    amount: float= Field(gt=0,description="Amount must be positive")
    
#create tables  
Base.metadata.create_all(bind=engine)

#innitialize fastapi
app = FastAPI()

#dependancy to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
   
#endpoint for creating account
@app.post('/account/create/')
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
        
#authentication route......
    
#endpoint for retriving spacific user data with id parameter
@app.get('/account/{account_id}')
async def fetch_acccount(account_id:int=Path(description="Account ID"), db:Session=Depends(get_db),response_model=create_account_base):
    _account=db.query(Account).filter(Account.id==account_id).first()
    if _account:
        return {
            'account Number': _account.account_number, 
            'email': _account.email, 
            'name': _account.name,
            'surname':_account.surname, 
            'balance': _account.balance,
            'account created':_account.creation_date}
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
#endpoint for updating information
@app.put('/account/{account_id}')
async def update_account(account_id:int = Path(description= "Updating Account ID"),account:create_account_base = Depends(),db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()

    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    existing_account.email  = account.email
    existing_account.name = account.name
    existing_account.surname = account.surname
    existing_account.balance = account.balance

    db.commit()
    db.refresh(existing_account)

    return {
            'account Number': existing_account.id, 
            'email': existing_account.email, 
            'name':existing_account.name,
            'surname':existing_account.surname, 
            'balance': existing_account.balance,}

        


#endpoint for deleting an account
@app.delete('/account/{account_id}')
async def update_account(account_id:int = Path(description= "Delete Account ID"),account:create_account_base = Depends(),db: Session = Depends(get_db)):
    existing_account = db.query(Account).filter(Account.id == account_id).first()

    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(existing_account)
    db.commit()

    return(f"Account_id{account_id} has been deleted successfully")



#endpoint for adding funds to account
@app.post('/account/{account_id}/deposit/')
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
@app.post('/account/{account_id}/withdraw')
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