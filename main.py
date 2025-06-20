from fastapi import FastAPI
from database import Base, engine
from routes import users, wallet, products

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(wallet.router)
app.include_router(products.router)
