from fastapi import APIRouter, HTTPException
from app.models.customer import get_all_customers, get_customer_by_id, add_customer, update_customer, delete_customer
from app.views.customer_schema import Customer, CustomerCreate

router = APIRouter()

@router.post("/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    # Add the customer to the database
    added_customer_id = add_customer(customer.name, customer.email)
    # Get the newly added customer by its ID
    new_customer = get_customer_by_id(added_customer_id)
    if new_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found after creation")
    # Return the customer as a Pydantic model
    return Customer(id=new_customer['CustomerID'], name=new_customer['Name'], email=new_customer['Email'])

@router.get("/", response_model=list[Customer])
async def read_customers():
    customers = get_all_customers()
    # Convert the query result to a list of Pydantic models
    return [Customer(id=customer['CustomerID'], name=customer['Name'], email=customer['Email']) for customer in customers]

@router.get("/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(id=customer['CustomerID'], name=customer['Name'], email=customer['Email'])

@router.put("/{customer_id}", response_model=Customer)
async def update_customer_details(customer_id: int, customer_update: CustomerCreate):
    updated = update_customer(customer_id, customer_update.name, customer_update.email)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    updated_customer = get_customer_by_id(customer_id)
    return Customer(id=updated_customer['CustomerID'], name=updated_customer['Name'], email=updated_customer['Email'])

@router.delete("/{customer_id}")
async def delete_customer_details(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(customer_id)
    return {"message": "Customer deleted successfully!"}