from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: str

class Customer(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True