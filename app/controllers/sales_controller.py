from fastapi import APIRouter, HTTPException
from datetime import date as date_type
from typing import List, Dict, Any
from app.models.sales import (
    get_all_sales, get_sale_by_id, add_sale, update_sale, delete_sale,
    get_sales_by_book, get_bestselling_authors, get_top_customers
)
from app.views.sales_schema import Sale, SaleCreate, SaleDetail

router = APIRouter()

@router.post("/", response_model=SaleDetail)
async def create_sale(sale: SaleCreate):
    # Add the sale to the database
    new_sale_id = add_sale(sale.book_id, sale.customer_id, sale.date, sale.quantity)
    # Get the newly added sale with details
    new_sale = get_sale_by_id(new_sale_id)
    if new_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found after creation")
    # Return the sale with details
    return SaleDetail(
        id=new_sale['SaleID'],
        book_id=new_sale['BookID'],
        book_title=new_sale['BookTitle'],
        book_price=new_sale['BookPrice'],
        customer_id=new_sale['CustomerID'],
        customer_name=new_sale['CustomerName'],
        date=new_sale['Date'],
        quantity=new_sale['Quantity'],
        total_amount=new_sale['TotalAmount']
    )

@router.get("/", response_model=List[SaleDetail])
async def read_sales():
    sales = get_all_sales()
    return [
        SaleDetail(
            id=sale['SaleID'],
            book_id=sale['BookID'],
            book_title=sale['BookTitle'],
            book_price=sale['BookPrice'],
            customer_id=sale['CustomerID'],
            customer_name=sale['CustomerName'],
            date=sale['Date'],
            quantity=sale['Quantity'],
            total_amount=sale['TotalAmount']
        ) for sale in sales
    ]

@router.get("/{sale_id}", response_model=SaleDetail)
async def read_sale(sale_id: int):
    sale = get_sale_by_id(sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return SaleDetail(
        id=sale['SaleID'],
        book_id=sale['BookID'],
        book_title=sale['BookTitle'],
        book_price=sale['BookPrice'],
        customer_id=sale['CustomerID'],
        customer_name=sale['CustomerName'],
        date=sale['Date'],
        quantity=sale['Quantity'],
        total_amount=sale['TotalAmount']
    )

@router.put("/{sale_id}", response_model=SaleDetail)
async def update_sale_details(sale_id: int, sale_update: SaleCreate):
    updated = update_sale(
        sale_id, sale_update.book_id, sale_update.customer_id, 
        sale_update.date, sale_update.quantity
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Sale not found")
    updated_sale = get_sale_by_id(sale_id)
    return SaleDetail(
        id=updated_sale['SaleID'],
        book_id=updated_sale['BookID'],
        book_title=updated_sale['BookTitle'],
        book_price=updated_sale['BookPrice'],
        customer_id=updated_sale['CustomerID'],
        customer_name=updated_sale['CustomerName'],
        date=updated_sale['Date'],
        quantity=updated_sale['Quantity'],
        total_amount=updated_sale['TotalAmount']
    )

@router.delete("/{sale_id}")
async def delete_sale_details(sale_id: int):
    sale = get_sale_by_id(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    delete_sale(sale_id)
    return {"message": "Sale deleted successfully!"}

# Analytics endpoints
@router.get("/analytics/by-book", response_model=List[Dict[str, Any]])
async def sales_by_book():
    result = get_sales_by_book()
    return [dict(row) for row in result]

@router.get("/analytics/bestselling-authors", response_model=List[Dict[str, Any]])
async def bestselling_authors():
    result = get_bestselling_authors()
    return [dict(row) for row in result]

@router.get("/analytics/top-customers", response_model=List[Dict[str, Any]])
async def top_customers():
    result = get_top_customers()
    return [dict(row) for row in result]