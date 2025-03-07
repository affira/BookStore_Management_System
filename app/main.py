# main.py
from fastapi import FastAPI
from app.controllers.book_controller import router as book_router
from app.controllers.customer_controller import router as customer_router

app = FastAPI(title="Bookstore Management System")

app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(customer_router, prefix="/customers", tags=["customers"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore Management API"}