from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    token_balance = relationship("TokenBalance", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")
    redemptions = relationship("Redemption", back_populates="user")

class Collectible(Base):
    __tablename__ = 'collectibles'
    id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)
    set_name = Column(String)  # Changed from 'set' to 'set_name'
    rarity = Column(String)
    edition = Column(String)
    metadata = Column(JSON)
    image_url = Column(String)
    current_price = Column(Float)

    price_history = relationship("PriceHistory", back_populates="collectible")
    redemptions = relationship("Redemption", back_populates="collectible")

class TokenBalance(Base):
    __tablename__ = 'token_balances'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    balance = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="token_balance")

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(String, primary_key=True)
    collectible_id = Column(String, ForeignKey("collectibles.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    price = Column(Float)
    source = Column(String)

    collectible = relationship("Collectible", back_populates="price_history")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String)
    amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)

    user = relationship("User", back_populates="transactions")

class Redemption(Base):
    __tablename__ = 'redemptions'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    collectible_id = Column(String, ForeignKey("collectibles.id"))
    tokens_spent = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    shipping_info = Column(JSON)
    status = Column(String)

    user = relationship("User", back_populates="redemptions")
    collectible = relationship("Collectible", back_populates="redemptions")
