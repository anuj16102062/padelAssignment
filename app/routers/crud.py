# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
import uuid

def create_account(db: Session, account: schemas.AccountCreate) -> models.Account:
    app_secret_token = str(uuid.uuid4())
    db_account = models.Account(
        email=account.email,
        account_name=account.account_name,
        app_secret_token=app_secret_token,
        website=account.website
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Add other CRUD operations as needed...
