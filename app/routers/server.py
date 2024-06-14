from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.requests import Request
from sqlalchemy.orm import Session
from app.models import Account, Destination
from app.database import SessionLocal
import httpx
import json

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/server/incoming_data")
async def incoming_data(data: dict, request: Request, db: Session = Depends(get_db)):
    cl_x_token = request.headers.get("cl_x_token")
    if not cl_x_token:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    db_account = db.query(Account).filter(Account.app_secret_token == cl_x_token).first()
    if not db_account:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    destinations = db_account.destinations
    
    print(destinations,'-------------27',data)
    
    async with httpx.AsyncClient() as client:
        for destination in destinations:
            try:
                headers = {"Content-Type": "application/json"}
                headers.update(json.loads(destination.headers))

                if destination.http_method.lower() == 'get':
                    response = await client.get(destination.url, params=data, headers=headers)
                elif destination.http_method.lower() in ['post', 'put']:
                    response = await client.request(
                        method=destination.http_method.lower(),
                        url=destination.url,
                        json=data,
                        headers=headers
                    )
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"Error decoding headers for destination {destination.id}")

    return {"status": "Data forwarded successfully"}
