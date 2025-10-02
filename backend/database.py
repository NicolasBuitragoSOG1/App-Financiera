from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance_app.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models following MVVM pattern

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    accounts = relationship("Account", back_populates="owner")
    transactions = relationship("Transaction", back_populates="user")
    goals = relationship("FinancialGoal", back_populates="user")

class BankingPlatform(Base):
    __tablename__ = "banking_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    platform_type = Column(String)  # bank, digital_wallet, investment, crypto
    logo_url = Column(String, nullable=True)
    api_endpoint = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    accounts = relationship("Account", back_populates="platform")

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform_id = Column(Integer, ForeignKey("banking_platforms.id"))
    account_name = Column(String)
    account_type = Column(String)  # checking, savings, credit, investment
    account_number = Column(String)
    current_balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="accounts")
    platform = relationship("BankingPlatform", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    transaction_type = Column(String)  # income, expense, transfer
    category = Column(String)
    amount = Column(Float)
    description = Column(Text)
    transaction_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

class FinancialGoal(Base):
    __tablename__ = "financial_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_name = Column(String)
    goal_type = Column(String)  # savings, debt_reduction, investment
    target_amount = Column(Float)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime)
    priority = Column(String, default="medium")  # high, medium, low
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")

class FinancialMetric(Base):
    __tablename__ = "financial_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    metric_name = Column(String)
    metric_value = Column(Float)
    metric_type = Column(String)  # monthly_income, monthly_expenses, savings_rate, etc.
    calculation_date = Column(DateTime, default=datetime.utcnow)
    period_start = Column(DateTime)
    period_end = Column(DateTime)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
