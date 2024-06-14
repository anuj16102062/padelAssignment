# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    account_name = Column(String, index=True)
    app_secret_token = Column(String, index=True)
    website = Column(String, nullable=True)

    destinations = relationship("Destination", back_populates="account")

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=True)
    http_method = Column(String, nullable=False)
    headers = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="destinations")
