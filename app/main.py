from fastapi import FastAPI
from app.database import engine
from app.routers import account, destination, server
from app.models import Base

app = FastAPI()

# Include all routers
app.include_router(account.router)
app.include_router(destination.router)
app.include_router(server.router)

# Create tables
Base.metadata.create_all(bind=engine)
