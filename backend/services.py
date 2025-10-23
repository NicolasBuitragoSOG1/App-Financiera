from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from database import User as DBUser, Account as DBAccount, Transaction as DBTransaction, FinancialGoal as DBFinancialGoal, FinancialMetric as DBFinancialMetric, BankingPlatform as DBBankingPlatform
from models import *
from auth import get_password_hash
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import HTTPException
# import pandas as pd  # Commented out temporarily
# import openai  # Commented out temporarily
import os
from dotenv import load_dotenv

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Commented out temporarily

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = DBUser(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(DBUser).filter(DBUser.email == email).first()

class BankingPlatformService:
    @staticmethod
    def create_platform(db: Session, platform: BankingPlatformCreate):
        db_platform = DBBankingPlatform(**platform.dict())
        db.add(db_platform)
        db.commit()
        db.refresh(db_platform)
        return db_platform

    @staticmethod
    def get_platforms(db: Session):
        return db.query(DBBankingPlatform).filter(DBBankingPlatform.is_active == True).all()

class AccountService:
    @staticmethod
    def create_account(db: Session, account: AccountCreate, user_id: int):
        db_account = DBAccount(**account.dict(), user_id=user_id)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account

    @staticmethod
    def get_user_accounts(db: Session, user_id: int):
        return db.query(DBAccount).filter(
            and_(DBAccount.user_id == user_id, DBAccount.is_active == True)
        ).all()

    @staticmethod
    def update_account_balance(db: Session, account_id: int, new_balance: float, user_id: int):
        account = db.query(DBAccount).filter(
            and_(DBAccount.id == account_id, DBAccount.user_id == user_id)
        ).first()
        if account:
            account.current_balance = new_balance
            account.last_updated = datetime.utcnow()
            db.commit()
            db.refresh(account)
        return account

    @staticmethod
    def update_account(db: Session, account_id: int, account_data: AccountCreate, user_id: int):
        account = db.query(DBAccount).filter(
            and_(DBAccount.id == account_id, DBAccount.user_id == user_id)
        ).first()
        if account:
            for key, value in account_data.dict().items():
                setattr(account, key, value)
            account.last_updated = datetime.utcnow()
            db.commit()
            db.refresh(account)
        return account

    @staticmethod
    def delete_account(db: Session, account_id: int, user_id: int):
        account = db.query(DBAccount).filter(
            and_(DBAccount.id == account_id, DBAccount.user_id == user_id)
        ).first()
        if account:
            account.is_active = False
            db.commit()
        return {"message": "Account deleted successfully"}

class TransactionService:
    @staticmethod
    def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
        # Validate transaction date is not in the future
        if transaction.transaction_date > datetime.utcnow():
            raise HTTPException(status_code=400, detail="No es posible agregar la transacción en una fecha futura")
        
        db_transaction = DBTransaction(**transaction.dict(), user_id=user_id)
        db.add(db_transaction)
        
        # Update account balance
        account = db.query(DBAccount).filter(DBAccount.id == transaction.account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Verify account belongs to user
        if account.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to use this account")
        
        # Check sufficient balance for expenses
        if transaction.transaction_type == TransactionType.EXPENSE:
            if account.current_balance < transaction.amount:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient balance. Available: ${account.current_balance:.2f}, Required: ${transaction.amount:.2f}"
                )
            account.current_balance -= transaction.amount
        elif transaction.transaction_type == TransactionType.INCOME:
            account.current_balance += transaction.amount
        
        account.last_updated = datetime.utcnow()
        
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def get_user_transactions(db: Session, user_id: int, limit: int = 50):
        return db.query(DBTransaction).filter(DBTransaction.user_id == user_id)\
            .order_by(DBTransaction.transaction_date.desc()).limit(limit).all()

    @staticmethod
    def get_transactions_by_period(db: Session, user_id: int, start_date: datetime, end_date: datetime):
        return db.query(DBTransaction).filter(
            and_(
                DBTransaction.user_id == user_id,
                DBTransaction.transaction_date >= start_date,
                DBTransaction.transaction_date <= end_date
            )
        ).all()

class FinancialGoalService:
    @staticmethod
    def create_goal(db: Session, goal: FinancialGoalCreate, user_id: int):
        db_goal = DBFinancialGoal(**goal.dict(), user_id=user_id)
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        return db_goal

    @staticmethod
    def get_user_goals(db: Session, user_id: int):
        return db.query(DBFinancialGoal).filter(
            and_(DBFinancialGoal.user_id == user_id, DBFinancialGoal.is_active == True)
        ).all()

    @staticmethod
    def update_goal_progress(db: Session, goal_id: int, current_amount: float, user_id: int):
        goal = db.query(DBFinancialGoal).filter(
            and_(DBFinancialGoal.id == goal_id, DBFinancialGoal.user_id == user_id)
        ).first()
        if goal:
            goal.current_amount = current_amount
            db.commit()
            db.refresh(goal)
        return goal

    @staticmethod
    def update_goal(db: Session, goal_id: int, goal_data: FinancialGoalCreate, user_id: int):
        goal = db.query(DBFinancialGoal).filter(
            and_(DBFinancialGoal.id == goal_id, DBFinancialGoal.user_id == user_id)
        ).first()
        if goal:
            for key, value in goal_data.dict().items():
                setattr(goal, key, value)
            db.commit()
            db.refresh(goal)
        return goal

    @staticmethod
    def delete_goal(db: Session, goal_id: int, user_id: int):
        goal = db.query(DBFinancialGoal).filter(
            and_(DBFinancialGoal.id == goal_id, DBFinancialGoal.user_id == user_id)
        ).first()
        if goal:
            goal.is_active = False
            db.commit()
        return {"message": "Goal deleted successfully"}

class FinancialAnalyticsService:
    @staticmethod
    def calculate_monthly_metrics(db: Session, user_id: int, month: int, year: int):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        transactions = TransactionService.get_transactions_by_period(db, user_id, start_date, end_date)
        
        monthly_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
        monthly_expenses = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0

        # Save metrics
        metrics = [
            DBFinancialMetric(
                user_id=user_id,
                metric_name="Monthly Income",
                metric_value=monthly_income,
                metric_type="monthly_income",
                period_start=start_date,
                period_end=end_date
            ),
            DBFinancialMetric(
                user_id=user_id,
                metric_name="Monthly Expenses",
                metric_value=monthly_expenses,
                metric_type="monthly_expenses",
                period_start=start_date,
                period_end=end_date
            ),
            DBFinancialMetric(
                user_id=user_id,
                metric_name="Savings Rate",
                metric_value=savings_rate,
                metric_type="savings_rate",
                period_start=start_date,
                period_end=end_date
            )
        ]

        for metric in metrics:
            db.add(metric)
        db.commit()

        return {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "savings_rate": savings_rate
        }

    @staticmethod
    def get_financial_overview(db: Session, user_id: int) -> FinancialOverview:
        # Get all accounts grouped by platform
        accounts = AccountService.get_user_accounts(db, user_id)
        total_balance = sum(account.current_balance for account in accounts)

        # Group accounts by platform
        platform_summaries = {}
        for account in accounts:
            platform_name = account.platform.name
            if platform_name not in platform_summaries:
                platform_summaries[platform_name] = {
                    "platform_name": platform_name,
                    "platform_type": account.platform.platform_type,
                    "total_balance": 0,
                    "account_count": 0,
                    "accounts": []
                }
            platform_summaries[platform_name]["total_balance"] += account.current_balance
            platform_summaries[platform_name]["account_count"] += 1
            platform_summaries[platform_name]["accounts"].append(account)

        # Get current month metrics
        current_date = datetime.now()
        current_metrics = FinancialAnalyticsService.calculate_monthly_metrics(
            db, user_id, current_date.month, current_date.year
        )

        # Get recent transactions
        recent_transactions = TransactionService.get_user_transactions(db, user_id, 10)

        # Get active goals
        active_goals = FinancialGoalService.get_user_goals(db, user_id)

        return FinancialOverview(
            total_balance=total_balance,
            monthly_income=current_metrics["monthly_income"],
            monthly_expenses=current_metrics["monthly_expenses"],
            savings_rate=current_metrics["savings_rate"],
            account_summaries=[AccountSummary(**summary) for summary in platform_summaries.values()],
            recent_transactions=recent_transactions,
            active_goals=active_goals
        )

class AIAssistantService:
    @staticmethod
    async def get_financial_advice(db: Session, user_id: int, query: str) -> AIResponse:
        import os
        from openai import OpenAI
        
        # Get user's financial overview for context
        overview = FinancialAnalyticsService.get_financial_overview(db, user_id)
        
        # Generate recommendations based on the financial data
        recommendations = []
        if overview.savings_rate < 20:
            recommendations.append("Consider increasing your savings rate to at least 20%")
        if overview.monthly_expenses > overview.monthly_income * 0.8:
            recommendations.append("Review your expenses to identify areas for cost reduction")
        if len(overview.active_goals) == 0:
            recommendations.append("Set specific financial goals to stay motivated")
        if len(overview.account_summaries) < 2:
            recommendations.append("Consider diversifying across multiple account types")
        
        # Prepare financial context for the AI
        financial_context = f"""
User's Financial Overview:
- Total Balance: ${overview.total_balance:,.2f}
- Monthly Income: ${overview.monthly_income:,.2f}
- Monthly Expenses: ${overview.monthly_expenses:,.2f}
- Savings Rate: {overview.savings_rate:.1f}%
- Active Financial Goals: {len(overview.active_goals)}
- Number of Accounts: {len(overview.account_summaries)} across different platforms
"""
        
        if len(overview.active_goals) > 0:
            financial_context += "\nActive Goals:\n"
            for goal in overview.active_goals[:3]:  # Show top 3 goals
                progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
                financial_context += f"- {goal.goal_name}: ${goal.current_amount:,.2f} / ${goal.target_amount:,.2f} ({progress:.1f}% complete)\n"
        
        # Check if OpenAI API key is configured
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != 'your-openai-api-key-here':
            # Use OpenAI API
            try:
                client = OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert financial advisor AI assistant. Provide helpful, practical, and personalized financial advice based on the user's financial data. Be concise (2-3 paragraphs), encouraging, and actionable. Use emojis sparingly for emphasis."
                        },
                        {
                            "role": "user",
                            "content": f"{financial_context}\n\nUser Question: {query}\n\nPlease provide specific advice based on my financial situation."
                        }
                    ],
                    max_tokens=400,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                
                return AIResponse(
                    response=ai_response,
                    recommendations=recommendations[:3],
                    confidence=0.95
                )
                
            except Exception as e:
                print(f"OpenAI API Error: {e}")
                # Fallback to rule-based system
        
        # Fallback: Rule-based responses (when no API key or API fails)
        query_lower = query.lower()
        
        if 'sav' in query_lower or 'save' in query_lower:
            response = f"Based on your current financial situation, you have a savings rate of {overview.savings_rate:.1f}%. Your monthly income is ${overview.monthly_income:,.2f} and expenses are ${overview.monthly_expenses:,.2f}. "
            if overview.savings_rate < 10:
                response += "I recommend focusing on reducing expenses and increasing your savings rate to at least 10-20%. Start by tracking all expenses and identifying areas where you can cut back."
            elif overview.savings_rate < 20:
                response += "You're making progress! Try to increase your savings rate to 20% for a healthier financial cushion. Consider automating your savings."
            else:
                response += "Excellent savings rate! Consider investing some of your savings for long-term growth."
                
        elif 'budget' in query_lower or 'expense' in query_lower or 'spend' in query_lower:
            response = f"Your current monthly expenses are ${overview.monthly_expenses:,.2f}, which is {(overview.monthly_expenses/overview.monthly_income*100):.1f}% of your income. "
            if overview.monthly_expenses > overview.monthly_income:
                response += "⚠️ Your expenses exceed your income. This is unsustainable. Review all expenses immediately and cut non-essential spending."
            elif overview.monthly_expenses > overview.monthly_income * 0.8:
                response += "You're spending a high percentage of your income. Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings."
            else:
                response += "Your expense ratio looks healthy. Keep tracking your spending and look for optimization opportunities."
                
        elif 'goal' in query_lower:
            response = f"You currently have {len(overview.active_goals)} active financial goals. "
            if len(overview.active_goals) == 0:
                response += "Setting specific goals is crucial for financial success. Consider creating goals for: emergency fund (3-6 months expenses), retirement savings, major purchases, or debt reduction."
            else:
                response += "Great job setting goals! Review them regularly and adjust contributions as your income grows. Breaking large goals into smaller milestones helps maintain motivation."
                
        elif 'invest' in query_lower:
            if overview.savings_rate < 10:
                response = "Before investing, focus on building an emergency fund covering 3-6 months of expenses. Once that's established, consider low-cost index funds for long-term growth."
            else:
                response = f"With a {overview.savings_rate:.1f}% savings rate, you may be ready to invest. Consider: 1) Max out retirement accounts (401k/IRA), 2) Low-cost index funds, 3) Diversify across stocks and bonds based on your risk tolerance."
                
        elif 'debt' in query_lower:
            response = "Debt management strategies: 1) Pay high-interest debt first (credit cards), 2) Consider debt avalanche or snowball method, 3) Avoid new debt while paying existing, 4) Look into debt consolidation if you have multiple loans."
            
        else:
            response = f"Here's an overview of your finances: Total Balance: ${overview.total_balance:,.2f}, Monthly Income: ${overview.monthly_income:,.2f}, Expenses: ${overview.monthly_expenses:,.2f}, Savings Rate: {overview.savings_rate:.1f}%. "
            if overview.savings_rate >= 20 and overview.monthly_expenses < overview.monthly_income:
                response += "Your finances look healthy! Focus on maintaining good habits and consider increasing investments for long-term growth."
            elif overview.savings_rate >= 10:
                response += "You're on the right track. Work on increasing your savings rate and setting specific financial goals."
            else:
                response += "There's room for improvement. Focus on reducing expenses, increasing income if possible, and building better savings habits."
        
        return AIResponse(
            response=response,
            recommendations=recommendations[:3],
            confidence=0.85
        )
