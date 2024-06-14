from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from app.models import Destination as DestinationModel
from app.schemas import DestinationCreate,Destination
from app.database import SessionLocal
from typing import Dict, Any,List
import json

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/destinations/", response_model=Dict[str, Any])
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    try:
        headers_json = json.dumps(destination.headers)
        
        db_destination = DestinationModel(
            url=str(destination.url) if destination.url else None,
            http_method=destination.http_method,
            headers=headers_json,
            account_id=destination.account_id
        )
        
        db.add(db_destination)
        db.commit()
        db.refresh(db_destination)
        
        # Load headers back from JSON string
        response_headers = json.loads(db_destination.headers)
        
        # Create the response dictionary
        response_destination = {
            "destination": {
                "id": db_destination.id,
                "url": db_destination.url,
                "http_method": db_destination.http_method,
                "headers": response_headers,
                "account_id": db_destination.account_id
            },
            "destination_id": db_destination.id  # Include the id separately if needed
        }
        
        return response_destination
    except Exception as e:
        print('Destination create error:', e)
        raise HTTPException(status_code=500, detail="Failed to create destination")

@router.get("/destinations/{destination_id}", response_model=Destination)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    response_headers = json.loads(db_destination.headers)
    return Destination(
        id=db_destination.id,
        url=db_destination.url,
        http_method=db_destination.http_method,
        headers=response_headers,
        account_id=db_destination.account_id
    )
@router.put("/destinations/{destination_id}", response_model=Dict[str, Any])
def update_destination(destination_id: int, destination_data: DestinationCreate, db: Session = Depends(get_db)):
    try:
        # Retrieve the destination from the database
        db_destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
        if not db_destination:
            raise HTTPException(status_code=404, detail=f"Destination with id {destination_id} not found")
        
        # Update the destination attributes based on the request data
        db_destination.url = str(destination_data.url) if destination_data.url else None
        db_destination.http_method = destination_data.http_method
        db_destination.headers = json.dumps(destination_data.headers)
        db_destination.account_id = destination_data.account_id
        
        db.commit()
        db.refresh(db_destination)
        
        response_headers = json.loads(db_destination.headers)
        
        response_destination = {
            "destination": {
                "id": db_destination.id,
                "url": db_destination.url,
                "http_method": db_destination.http_method,
                "headers": response_headers,
                "account_id": db_destination.account_id
            },
            "destination_id": db_destination.id 
        }
        
        return response_destination
    except Exception as e:
        print('Destination update error:', e)
        raise HTTPException(status_code=500, detail=f"Failed to update destination with id {destination_id}")
@router.get("/destinations/")
def get_destinations_raw(db: Session = Depends(get_db)):
    destinations = db.query(DestinationModel).all()
    return destinations