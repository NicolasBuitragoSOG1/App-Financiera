from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums for better type safety
class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    INVESTMENT = "investment"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class PlatformType(str, Enum):
    BANK = "bank"
    DIGITAL_WALLET = "digital_wallet"
    INVESTMENT = "investment"
    CRYPTO = "crypto"

class GoalType(str, Enum):
    SAVINGS = "savings"
    DEBT_REDUCTION = "debt_reduction"
    INVESTMENT = "investment"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Pydantic models for API requests/responses (ViewModels in MVVM)

# User models
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Banking Platform models
class BankingPlatformBase(BaseModel):
    name: str
    platform_type: PlatformType
    logo_url: Optional[str] = None
    api_endpoint: Optional[str] = None

class BankingPlatformCreate(BankingPlatformBase):
    pass

class BankingPlatform(BankingPlatformBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# Account models
class AccountBase(BaseModel):
    account_name: str
    account_type: AccountType
    account_number: str
    current_balance: float = 0.0
    currency: str = "USD"

class AccountCreate(AccountBase):
    platform_id: int

class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    current_balance: Optional[float] = None
    is_active: Optional[bool] = None

class Account(AccountBase):
    id: int
    user_id: int
    platform_id: int
    is_active: bool
    created_at: datetime
    last_updated: datetime
    platform: BankingPlatform
    
    class Config:
        from_attributes = True

# Transaction models
class TransactionBase(BaseModel):
    transaction_type: TransactionType
    category: str
    amount: float
    description: str
    transaction_date: datetime

class TransactionCreate(TransactionBase):
    account_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int
    account_id: int
    created_at: datetime
    account: Account
    
    class Config:
        from_attributes = True

# Financial Goal models
class FinancialGoalBase(BaseModel):
    goal_name: str
    goal_type: GoalType
    target_amount: float
    target_date: datetime
    priority: Priority = Priority.MEDIUM

class FinancialGoalCreate(FinancialGoalBase):
    pass

class FinancialGoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    is_active: Optional[bool] = None

class FinancialGoal(FinancialGoalBase):
    id: int
    user_id: int
    current_amount: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Financial Metrics models
class FinancialMetricBase(BaseModel):
    metric_name: str
    metric_value: float
    metric_type: str
    period_start: datetime
    period_end: datetime

class FinancialMetric(FinancialMetricBase):
    id: int
    user_id: int
    calculation_date: datetime
    
    class Config:
        from_attributes = True

# Dashboard models
class AccountSummary(BaseModel):
    platform_name: str
    platform_type: str
    total_balance: float
    account_count: int
    accounts: List[Account]

class FinancialOverview(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    account_summaries: List[AccountSummary]
    recent_transactions: List[Transaction]
    active_goals: List[FinancialGoal]

# AI Assistant models
class AIQuery(BaseModel):
    query: str
    context: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    recommendations: List[str]
    confidence: float

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str
