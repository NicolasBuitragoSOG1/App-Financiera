from database import SessionLocal, Transaction as DBTransaction, User as DBUser
from datetime import datetime

db = SessionLocal()

user = db.query(DBUser).filter(DBUser.email == 'user@test.com').first()
if not user:
    print("User not found!")
    db.close()
    exit()

print(f"User ID: {user.id}")

transactions = db.query(DBTransaction).filter(DBTransaction.user_id == user.id).all()
print(f"\nTotal transactions: {len(transactions)}")

expenses = [t for t in transactions if t.transaction_type == 'expense']
incomes = [t for t in transactions if t.transaction_type == 'income']

print(f"Expense transactions: {len(expenses)}")
print(f"Income transactions: {len(incomes)}")

if expenses:
    print(f"\nSample expense: {expenses[0].category} - ${expenses[0].amount} - {expenses[0].transaction_date}")
    
    # Group by category
    categories = {}
    for t in expenses:
        if t.category in categories:
            categories[t.category] += t.amount
        else:
            categories[t.category] = t.amount
    
    print("\nExpenses by category:")
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: ${amount:.2f}")

if incomes:
    print(f"\nSample income: {incomes[0].category} - ${incomes[0].amount} - {incomes[0].transaction_date}")
    
    total_income = sum(t.amount for t in incomes)
    total_expenses = sum(t.amount for t in expenses)
    print(f"\nTotal income: ${total_income:.2f}")
    print(f"Total expenses: ${total_expenses:.2f}")
    print(f"Net: ${total_income - total_expenses:.2f}")

db.close()
