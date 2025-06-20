import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Transaction
from schemas import PayRequest, BalanceResponse, TransactionResponse
from auth import get_db, get_current_user

router = APIRouter()

@router.post("/pay", response_model=BalanceResponse)
def pay(request: PayRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipient = db.query(User).filter(User.username == request.to).first()
    if not recipient or request.amt > user.balance:
        raise HTTPException(status_code=400, detail="Invalid recipient or insufficient balance")
    
    user.balance -= request.amt
    recipient.balance += request.amt
    
    db.add(Transaction(user=user, kind="debit", amt=request.amt, updated_bal=user.balance))
    db.add(Transaction(user=recipient, kind="credit", amt=request.amt, updated_bal=recipient.balance))
    db.commit()
    return {"balance": user.balance}

@router.get("/bal", response_model=BalanceResponse)
def get_balance(currency: str = "INR", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if currency.upper() != "INR":
        res = httpx.get(f"https://api.currencyapi.com/v3/latest?apikey=YOUR_API_KEY&base_currency=INR")
        rate = res.json()["data"].get(currency.upper())
        if not rate:
            raise HTTPException(status_code=400, detail="Currency not supported")
        return {"balance": round(user.balance * rate["value"], 2), "currency": currency.upper()}
    return {"balance": user.balance, "currency": "INR"}

@router.get("/stmt", response_model=list[TransactionResponse])
def transaction_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(Transaction.user_id == user.id).order_by(Transaction.timestamp.desc()).all()
    return txs
