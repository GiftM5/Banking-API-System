from fastapi import FastAPI, Depends,Path
from database.data import engine, Base,SessionLocal
from database.models.table import Account,Transaction
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

#pydantic models
class create_account_base(BaseModel):
    email: str
    name:str
    surname:str
    
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
async def create_account(account:create_account_base, db:Session=Depends(get_db)):
    email_match=db.query(Account).filter(Account.email==account.email).first()
    if email_match:
        return {'message':'Account with this email already exist'}
    else:
        new_acc=Account(email=account.email,name=account.name,surname=account.surname)
        db.add(new_acc)
        db.commit()
        db.refresh
        return{"message": 'account created','email':account.email}
    
#endpoint for retriving spacific user data with id parameter
@app.get('/account/{account_id}')
async def fetch_acccount(account_id:int=Path(description="Account ID"), db:Session=Depends(get_db)):
    _account=db.query(Account).filter(Account.id==account_id).first()
    if _account:
        return {'account Number': _account.account_number, 'email': _account.email, 'name': _account.name,'surname':_account.surname, 'balance': _account.balance,'account created':_account.creation_date}
    else:
        return {'mssage':'Account not found'}
    
#endpoint for updating information


#endpoint for deleting an account 


#endpoint for adding funds to account


#endpoint for withdrawing fund from account