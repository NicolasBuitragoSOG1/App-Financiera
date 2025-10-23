from sqlalchemy.orm import Session
from database import SessionLocal, User as DBUser, Account as DBAccount, Transaction as DBTransaction
from datetime import datetime, timedelta
import random

def add_demo_transactions():
    db = SessionLocal()
    
    # Get test user
    user = db.query(DBUser).filter(DBUser.email == "user@test.com").first()
    if not user:
        print("Test user not found.")
        db.close()
        return
    
    # Get user's accounts
    accounts = db.query(DBAccount).filter(DBAccount.user_id == user.id, DBAccount.is_active == True).all()
    if not accounts:
        print("No accounts found for user. Create accounts first.")
        db.close()
        return
    
    main_account = accounts[0]
    print(f"Using account: {main_account.account_name}")
    
    # Transaction categories
    income_categories = ['Salary', 'Freelance', 'Investment', 'Business']
    expense_categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 
                         'Bills & Utilities', 'Healthcare', 'Education', 'Personal Care']
    
    transactions_created = 0
    
    # Generate transactions for last 6 months
    for month_offset in range(6):
        target_date = datetime.now() - timedelta(days=30 * month_offset)
        
        # Monthly salary (2 times per month)
        for _ in range(2):
            salary_transaction = DBTransaction(
                user_id=user.id,
                account_id=main_account.id,
                transaction_type="income",
                amount=random.uniform(2000, 2500),
                category="Salary",
                description="Monthly Salary",
                transaction_date=target_date - timedelta(days=random.randint(0, 28))
            )
            db.add(salary_transaction)
            transactions_created += 1
        
        # Random freelance income
        if random.random() > 0.4:
            freelance_transaction = DBTransaction(
                user_id=user.id,
                account_id=main_account.id,
                transaction_type="income",
                amount=random.uniform(500, 1500),
                category="Freelance",
                description="Freelance Project Payment",
                transaction_date=target_date - timedelta(days=random.randint(0, 28))
            )
            db.add(freelance_transaction)
            transactions_created += 1
        
        # Random expenses throughout the month
        num_expenses = random.randint(20, 30)
        for _ in range(num_expenses):
            category = random.choice(expense_categories)
            
            # Realistic amounts per category
            amount_ranges = {
                'Food & Dining': (15, 120),
                'Transportation': (20, 80),
                'Shopping': (40, 250),
                'Entertainment': (25, 150),
                'Bills & Utilities': (80, 350),
                'Healthcare': (50, 300),
                'Education': (100, 500),
                'Personal Care': (20, 100)
            }
            
            min_amt, max_amt = amount_ranges.get(category, (20, 150))
            amount = random.uniform(min_amt, max_amt)
            
            expense_transaction = DBTransaction(
                user_id=user.id,
                account_id=main_account.id,
                transaction_type="expense",
                amount=round(amount, 2),
                category=category,
                description=f"{category} purchase",
                transaction_date=target_date - timedelta(days=random.randint(0, 28))
            )
            db.add(expense_transaction)
            transactions_created += 1
    
    db.commit()
    print(f"Successfully created {transactions_created} demo transactions!")
    print(f"Total transactions in database: {db.query(DBTransaction).filter(DBTransaction.user_id == user.id).count()}")
    print("\nNow you can see the Analytics charts with real data!")
    print("Go to Analytics section and select current month/year to see the graphs.")
    db.close()

if __name__ == "__main__":
    print("Adding demo transactions...")
    add_demo_transactions()
