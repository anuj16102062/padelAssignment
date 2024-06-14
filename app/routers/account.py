from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Account as AccountModel, Destination as DestinationModel
from app.schemas import AccountCreate, Account, DestinationCreate, Destination
from app.database import SessionLocal
from typing import List
import uuid
import json

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accounts/", response_model=Account)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    try:
        token = str(uuid.uuid4())
        db_account = AccountModel(
            email=account.email,
            account_name=account.account_name,
            app_secret_token=token,
            website=str(account.website) if account.website else None
        )
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        print(e, '------------37')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/accounts/{account_id}", response_model=dict)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Delete associated destinations
    db.query(DestinationModel).filter(DestinationModel.account_id == account_id).delete()
    
    db.delete(db_account)
    db.commit()
    return {"message": "Account deleted successfully"}

@router.get("/accounts/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    print(db_account,'---------56')
    db_destinations = db.query(DestinationModel).filter(DestinationModel.account_id == account_id).all()
    for dest in db_destinations:
        dest.headers = json.loads(dest.headers)
    account_with_destinations = Account(
        id=db_account.id,
        email=db_account.email,
        account_name=db_account.account_name,
        app_secret_token=db_account.app_secret_token,
        website=db_account.website,
        destinations=[
            Destination(
                id=dest.id,
                url=dest.url,
                http_method=dest.http_method,
                headers=dest.headers,
                account_id=dest.account_id
            ) for dest in db_destinations
        ]
    )
    
    return account_with_destinations

@router.get("/accounts/{account_id}/destinations/", response_model=list[Destination])
def read_destinations_for_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    destinations = db.query(DestinationModel).filter(DestinationModel.account_id == account_id).all()
    for dest in destinations:
        dest.headers = json.loads(dest.headers)
    return destinations