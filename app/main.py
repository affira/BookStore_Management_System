from fastapi import FastAPI
from app.controllers.book_controller import router as book_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.sales_controller import router as sale_router

app = FastAPI(title="Bookstore Management System")

app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(customer_router, prefix="/customers", tags=["customers"])
app.include_router(sale_router, prefix="/sales", tags=["sales"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore Management API"}