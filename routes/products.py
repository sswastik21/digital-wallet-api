from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product, User, Transaction
from schemas import ProductCreate, ProductOut, BuyRequest
from auth import get_current_user, get_db

router = APIRouter()

@router.post("/product", response_model=dict, status_code=201)
def add_product(product: ProductCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    p = Product(**product.dict())
    db.add(p)
    db.commit()
    return {"id": p.id, "message": "Product added"}

@router.get("/product", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/buy", response_model=dict)
def buy_product(request: BuyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product or product.price > user.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance or invalid product")
    user.balance -= product.price
    db.add(Transaction(user=user, kind="debit", amt=product.price, updated_bal=user.balance))
    db.commit()
    return {"message": "Product purchased", "balance": user.balance}
