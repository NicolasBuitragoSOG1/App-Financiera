from sqlalchemy.orm import Session
from database import SessionLocal, BankingPlatform as DBBankingPlatform, User as DBUser, Account as DBAccount, Transaction as DBTransaction, FinancialGoal as DBFinancialGoal
from auth import get_password_hash
from datetime import datetime, timedelta
import random

def init_banking_platforms():
    db = SessionLocal()
    
    # Check if platforms already exist
    existing_platforms = db.query(DBBankingPlatform).count()
    if existing_platforms > 0:
        print("Banking platforms already initialized")
        db.close()
        return
    
    platforms = [
        # Traditional Banks
        {"name": "Bank of America", "platform_type": "bank", "logo_url": "/logos/boa.png"},
        {"name": "Chase", "platform_type": "bank", "logo_url": "/logos/chase.png"},
        {"name": "Wells Fargo", "platform_type": "bank", "logo_url": "/logos/wells.png"},
        {"name": "Citibank", "platform_type": "bank", "logo_url": "/logos/citi.png"},
        {"name": "HSBC", "platform_type": "bank", "logo_url": "/logos/hsbc.png"},
        
        # Digital Wallets
        {"name": "PayPal", "platform_type": "digital_wallet", "logo_url": "/logos/paypal.png"},
        {"name": "Venmo", "platform_type": "digital_wallet", "logo_url": "/logos/venmo.png"},
        {"name": "Cash App", "platform_type": "digital_wallet", "logo_url": "/logos/cashapp.png"},
        {"name": "Apple Pay", "platform_type": "digital_wallet", "logo_url": "/logos/applepay.png"},
        {"name": "Google Pay", "platform_type": "digital_wallet", "logo_url": "/logos/googlepay.png"},
        
        # Investment Platforms
        {"name": "Fidelity", "platform_type": "investment", "logo_url": "/logos/fidelity.png"},
        {"name": "Charles Schwab", "platform_type": "investment", "logo_url": "/logos/schwab.png"},
        {"name": "E*TRADE", "platform_type": "investment", "logo_url": "/logos/etrade.png"},
        {"name": "Robinhood", "platform_type": "investment", "logo_url": "/logos/robinhood.png"},
        {"name": "TD Ameritrade", "platform_type": "investment", "logo_url": "/logos/tdameritrade.png"},
        
        # Crypto Platforms
        {"name": "Coinbase", "platform_type": "crypto", "logo_url": "/logos/coinbase.png"},
        {"name": "Binance", "platform_type": "crypto", "logo_url": "/logos/binance.png"},
        {"name": "Kraken", "platform_type": "crypto", "logo_url": "/logos/kraken.png"},
        {"name": "Gemini", "platform_type": "crypto", "logo_url": "/logos/gemini.png"},
    ]
    
    for platform_data in platforms:
        platform = DBBankingPlatform(**platform_data)
        db.add(platform)
    
    db.commit()
    print(f"Initialized {len(platforms)} banking platforms")
    db.close()

def create_test_user():
    db = SessionLocal()
    
    # Check if test user already exists
    existing_user = db.query(DBUser).filter(DBUser.email == "user@test.com").first()
    if existing_user:
        print("Test user already exists")
        db.close()
        return
    
    # Create test user
    test_user = DBUser(
        email="user@test.com",
        hashed_password=get_password_hash("Test123"),
        full_name="Test User"
    )
    
    db.add(test_user)
    db.commit()
    print("Created test user: user@test.com / Test123")
    db.close()

def create_demo_data():
    db = SessionLocal()
    
    # Get test user
    user = db.query(DBUser).filter(DBUser.email == "user@test.com").first()
    if not user:
        print("Test user not found. Run create_test_user() first.")
        db.close()
        return
    
    # Check if demo data already exists
    existing_accounts = db.query(DBAccount).filter(DBAccount.user_id == user.id).count()
    if existing_accounts > 0:
        print("Demo data already exists")
        db.close()
        return
    
    # Get platforms
    bank_platform = db.query(DBBankingPlatform).filter(DBBankingPlatform.name == "Chase").first()
    wallet_platform = db.query(DBBankingPlatform).filter(DBBankingPlatform.name == "PayPal").first()
    
    if not bank_platform or not wallet_platform:
        print("Banking platforms not found. Run init_banking_platforms() first.")
        db.close()
        return
    
    # Create demo accounts
    checking_account = DBAccount(
        user_id=user.id,
        platform_id=bank_platform.id,
        account_name="Main Checking",
        account_type="checking",
        account_number="****1234",
        current_balance=5000.00,
        currency="USD"
    )
    
    savings_account = DBAccount(
        user_id=user.id,
        platform_id=bank_platform.id,
        account_name="Savings Account",
        account_type="savings",
        account_number="****5678",
        current_balance=15000.00,
        currency="USD"
    )
    
    wallet_account = DBAccount(
        user_id=user.id,
        platform_id=wallet_platform.id,
        account_name="PayPal Wallet",
        account_type="checking",
        account_number="****9012",
        current_balance=1500.00,
        currency="USD"
    )
    
    db.add_all([checking_account, savings_account, wallet_account])
    db.commit()
    db.refresh(checking_account)
    
    # Create demo transactions for the last 6 months
    income_categories = ['Salary', 'Freelance', 'Investment', 'Business']
    expense_categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 
                         'Bills & Utilities', 'Healthcare', 'Education']
    
    transactions_created = 0
    
    # Generate transactions for last 6 months
    for month_offset in range(6):
        target_date = datetime.now() - timedelta(days=30 * month_offset)
        
        # Monthly salary
        salary_transaction = DBTransaction(
            user_id=user.id,
            account_id=checking_account.id,
            transaction_type="income",
            amount=random.uniform(4000, 5000),
            category="Salary",
            description="Monthly Salary",
            transaction_date=target_date - timedelta(days=random.randint(0, 5))
        )
        db.add(salary_transaction)
        transactions_created += 1
        
        # Random freelance income
        if random.random() > 0.5:
            freelance_transaction = DBTransaction(
                user_id=user.id,
                account_id=wallet_account.id,
                transaction_type="income",
                amount=random.uniform(500, 1500),
                category="Freelance",
                description="Freelance Project",
                transaction_date=target_date - timedelta(days=random.randint(0, 28))
            )
            db.add(freelance_transaction)
            transactions_created += 1
        
        # Random expenses throughout the month
        num_expenses = random.randint(15, 25)
        for _ in range(num_expenses):
            category = random.choice(expense_categories)
            amount = 0
            
            if category == 'Food & Dining':
                amount = random.uniform(20, 150)
            elif category == 'Transportation':
                amount = random.uniform(30, 100)
            elif category == 'Shopping':
                amount = random.uniform(50, 300)
            elif category == 'Bills & Utilities':
                amount = random.uniform(100, 400)
            else:
                amount = random.uniform(30, 200)
            
            expense_transaction = DBTransaction(
                user_id=user.id,
                account_id=checking_account.id,
                transaction_type="expense",
                amount=amount,
                category=category,
                description=f"{category} expense",
                transaction_date=target_date - timedelta(days=random.randint(0, 28))
            )
            db.add(expense_transaction)
            transactions_created += 1
    
    # Create demo goals
    emergency_goal = DBFinancialGoal(
        user_id=user.id,
        goal_name="Emergency Fund",
        goal_type="savings",
        target_amount=20000.00,
        current_amount=15000.00,
        target_date=datetime.now() + timedelta(days=365),
        priority="high"
    )
    
    vacation_goal = DBFinancialGoal(
        user_id=user.id,
        goal_name="Vacation Fund",
        goal_type="savings",
        target_amount=5000.00,
        current_amount=2500.00,
        target_date=datetime.now() + timedelta(days=180),
        priority="medium"
    )
    
    db.add_all([emergency_goal, vacation_goal])
    
    db.commit()
    print(f"Created 3 demo accounts")
    print(f"Created {transactions_created} demo transactions")
    print(f"Created 2 demo financial goals")
    db.close()

if __name__ == "__main__":
    print("Initializing database with sample data...")
    init_banking_platforms()
    create_test_user()
    create_demo_data()
    print("Database initialization complete!")
