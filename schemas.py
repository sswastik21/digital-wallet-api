from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class FundRequest(BaseModel):
    amt: float

class PayRequest(BaseModel):
    to: str
    amt: float

class BalanceResponse(BaseModel):
    balance: float
    currency: Optional[str] = "INR"

class TransactionResponse(BaseModel):
    kind: str
    amt: float
    updated_bal: float
    timestamp: datetime

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: str

class BuyRequest(BaseModel):
    product_id: int
