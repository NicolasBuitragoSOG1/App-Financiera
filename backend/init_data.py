from sqlalchemy.orm import Session
from database import SessionLocal, BankingPlatform as DBBankingPlatform, User as DBUser
from auth import get_password_hash

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

if __name__ == "__main__":
    print("Initializing database with sample data...")
    init_banking_platforms()
    create_test_user()
    print("Database initialization complete!")
