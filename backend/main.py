from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

from database import get_db, create_tables
from models import *
from auth import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from services import *

# Create FastAPI app
app = FastAPI(
    title="Personal Finance Management API",
    description="API for managing personal finances with MVVM architecture",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Authentication endpoints
@app.post("/api/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return UserService.create_user(db=db, user=user)

@app.post("/api/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Banking Platform endpoints
@app.post("/api/platforms", response_model=BankingPlatform)
def create_platform(
    platform: BankingPlatformCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return BankingPlatformService.create_platform(db=db, platform=platform)

@app.get("/api/platforms", response_model=List[BankingPlatform])
def get_platforms(db: Session = Depends(get_db)):
    return BankingPlatformService.get_platforms(db)

# Account endpoints
@app.post("/api/accounts", response_model=Account)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return AccountService.create_account(db=db, account=account, user_id=current_user.id)

@app.get("/api/accounts", response_model=List[Account])
def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return AccountService.get_user_accounts(db, current_user.id)

@app.put("/api/accounts/{account_id}/balance")
def update_account_balance(
    account_id: int,
    balance_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return AccountService.update_account_balance(
        db, account_id, balance_update["new_balance"], current_user.id
    )

# Transaction endpoints
@app.post("/api/transactions", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return TransactionService.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return TransactionService.get_user_transactions(db, current_user.id, limit)

# Financial Goals endpoints
@app.post("/api/goals", response_model=FinancialGoal)
def create_goal(
    goal: FinancialGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialGoalService.create_goal(db=db, goal=goal, user_id=current_user.id)

@app.get("/api/goals", response_model=List[FinancialGoal])
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialGoalService.get_user_goals(db, current_user.id)

@app.put("/api/goals/{goal_id}/progress")
def update_goal_progress(
    goal_id: int,
    progress_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialGoalService.update_goal_progress(
        db, goal_id, progress_update["current_amount"], current_user.id
    )

@app.put("/api/goals/{goal_id}", response_model=FinancialGoal)
def update_goal(
    goal_id: int,
    goal: FinancialGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialGoalService.update_goal(db, goal_id, goal, current_user.id)

@app.delete("/api/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialGoalService.delete_goal(db, goal_id, current_user.id)

# Analytics endpoints
@app.get("/api/analytics/overview", response_model=FinancialOverview)
def get_financial_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialAnalyticsService.get_financial_overview(db, current_user.id)

@app.get("/api/analytics/monthly/{year}/{month}")
def get_monthly_metrics(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return FinancialAnalyticsService.calculate_monthly_metrics(db, current_user.id, month, year)

# AI Assistant endpoints
@app.post("/api/ai/advice", response_model=AIResponse)
async def get_financial_advice(
    query: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await AIAssistantService.get_financial_advice(db, current_user.id, query.query)

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Personal Finance API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
