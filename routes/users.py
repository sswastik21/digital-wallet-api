from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, FundRequest, BalanceResponse
from utils import hash_password
from auth import get_db, get_current_user

router = APIRouter()

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username exists")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

@router.post("/fund", response_model=BalanceResponse)
def fund_wallet(request: FundRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.balance += request.amt
    db.commit()
    return {"balance": user.balance}
