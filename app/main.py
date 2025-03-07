from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.book_controller import router as book_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.sales_controller import router as sale_router

app = FastAPI(title="Bookstore Management System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(customer_router, prefix="/customers", tags=["customers"])
app.include_router(sale_router, prefix="/sales", tags=["sales"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore Management API"}