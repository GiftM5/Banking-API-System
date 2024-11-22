from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from account import account_router
from transaction import transactions_router
from page import pages_router

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(account_router)
app.include_router(transactions_router)
app.include_router(pages_router)
