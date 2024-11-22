from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.data import get_db
from database.models.table import Account,Transaction
from connect import templates

pages_router = APIRouter(tags=["Pages"])

# route for home page.
@pages_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint for handling the form submission
@pages_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, name: str = Form(...), surname: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    # Check if account exists in the database with the provided name, surname, and email
    user = db.query(Account).filter(Account.name == name, Account.surname == surname, Account.email == email).first()
    
    # If account is not found, raise an HTTP exception
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Redirect to the detail page with the user's account ID
    return RedirectResponse(url=f"/detail/{user.id}", status_code=303)

# route for detail page.
@pages_router.get("/detail/{account_id}", response_class=HTMLResponse)
async def details_page(request: Request, account_id: int, db: Session = Depends(get_db)):
    user = db.query(Account).filter(Account.id == account_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return templates.TemplateResponse("details.html", {"request": request, "account": user})

# Creating account page.

# Updating account page.

# Deleting account page.

# Deposit page.

# Withdraw page.
