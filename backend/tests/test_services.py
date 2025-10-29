import pytest
from datetime import date, timedelta
from services import (
    UserService,
    AccountService,
    TransactionService,
    FinancialGoalService,
    AnalyticsService
)


class TestUserService:
    """Pruebas para UserService"""

    def test_create_user(self, db_session):
        """Prueba crear usuario"""
        user = UserService.create_user(
            db=db_session,
            email="service@example.com",
            password="password123",
            full_name="Service User"
        )
        assert user.id is not None
        assert user.email == "service@example.com"
        assert user.full_name == "Service User"
        assert user.is_active is True

    def test_get_user_by_email(self, db_session, test_user):
        """Prueba obtener usuario por email"""
        user = UserService.get_user_by_email(db_session, test_user.email)
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id(self, db_session, test_user):
        """Prueba obtener usuario por ID"""
        user = UserService.get_user_by_id(db_session, test_user.id)
        assert user is not None
        assert user.id == test_user.id


class TestAccountService:
    """Pruebas para AccountService"""

    def test_create_account(self, db_session, test_user, test_platform):
        """Prueba crear cuenta"""
        account = AccountService.create_account(
            db=db_session,
            user_id=test_user.id,
            platform_id=test_platform.id,
            account_name="Service Account",
            account_type="savings",
            current_balance=2000.00,
            currency="USD"
        )
        assert account.id is not None
        assert account.account_name == "Service Account"
        assert account.current_balance == 2000.00

    def test_get_user_accounts(self, db_session, test_user, test_account):
        """Prueba obtener cuentas de usuario"""
        accounts = AccountService.get_user_accounts(db_session, test_user.id)
        assert len(accounts) >= 1
        assert accounts[0].user_id == test_user.id

    def test_update_balance(self, db_session, test_account):
        """Prueba actualizar balance"""
        new_balance = 1500.00
        updated_account = AccountService.update_balance(
            db_session,
            test_account.id,
            new_balance
        )
        assert updated_account.current_balance == new_balance

    def test_delete_account(self, db_session, test_account):
        """Prueba eliminar cuenta"""
        result = AccountService.delete_account(db_session, test_account.id)
        assert result is True
        account = AccountService.get_account_by_id(db_session, test_account.id)
        assert account is None


class TestTransactionService:
    """Pruebas para TransactionService"""

    def test_create_transaction_income(self, db_session, test_user, test_account):
        """Prueba crear transacción de ingreso"""
        initial_balance = test_account.current_balance
        transaction = TransactionService.create_transaction(
            db=db_session,
            user_id=test_user.id,
            account_id=test_account.id,
            transaction_type="income",
            amount=500.00,
            category="salary",
            description="Test income",
            transaction_date=date.today()
        )
        assert transaction.id is not None
        assert transaction.amount == 500.00
        
        # Verificar que el balance se actualizó
        db_session.refresh(test_account)
        assert test_account.current_balance == initial_balance + 500.00

    def test_create_transaction_expense(self, db_session, test_user, test_account):
        """Prueba crear transacción de gasto"""
        initial_balance = test_account.current_balance
        transaction = TransactionService.create_transaction(
            db=db_session,
            user_id=test_user.id,
            account_id=test_account.id,
            transaction_type="expense",
            amount=200.00,
            category="food",
            description="Test expense",
            transaction_date=date.today()
        )
        assert transaction.id is not None
        
        # Verificar que el balance se actualizó
        db_session.refresh(test_account)
        assert test_account.current_balance == initial_balance - 200.00

    def test_validate_date_future(self, db_session):
        """Prueba validación de fecha futura"""
        future_date = date.today() + timedelta(days=1)
        with pytest.raises(ValueError, match="future"):
            TransactionService.validate_date(future_date)

    def test_validate_balance_insufficient(self, db_session, test_account):
        """Prueba validación de balance insuficiente"""
        with pytest.raises(ValueError, match="Insufficient balance"):
            TransactionService.validate_balance(
                test_account.current_balance,
                test_account.current_balance + 100.00
            )

    def test_get_user_transactions(self, db_session, test_user):
        """Prueba obtener transacciones de usuario"""
        transactions = TransactionService.get_user_transactions(
            db_session,
            test_user.id
        )
        assert isinstance(transactions, list)


class TestFinancialGoalService:
    """Pruebas para FinancialGoalService"""

    def test_create_goal(self, db_session, test_user):
        """Prueba crear meta financiera"""
        target_date = date.today() + timedelta(days=365)
        goal = FinancialGoalService.create_goal(
            db=db_session,
            user_id=test_user.id,
            goal_name="Emergency Fund",
            goal_type="savings",
            target_amount=10000.00,
            current_amount=0.00,
            priority="high",
            target_date=target_date
        )
        assert goal.id is not None
        assert goal.goal_name == "Emergency Fund"
        assert goal.target_amount == 10000.00

    def test_update_goal_progress(self, db_session, test_user):
        """Prueba actualizar progreso de meta"""
        target_date = date.today() + timedelta(days=365)
        goal = FinancialGoalService.create_goal(
            db=db_session,
            user_id=test_user.id,
            goal_name="Vacation Fund",
            goal_type="savings",
            target_amount=5000.00,
            current_amount=1000.00,
            priority="medium",
            target_date=target_date
        )
        
        updated_goal = FinancialGoalService.update_goal_progress(
            db_session,
            goal.id,
            2500.00
        )
        assert updated_goal.current_amount == 2500.00

    def test_get_user_goals(self, db_session, test_user):
        """Prueba obtener metas de usuario"""
        goals = FinancialGoalService.get_user_goals(db_session, test_user.id)
        assert isinstance(goals, list)


class TestAnalyticsService:
    """Pruebas para AnalyticsService"""

    def test_calculate_monthly_metrics(self, db_session, test_user, test_account):
        """Prueba calcular métricas mensuales"""
        # Crear algunas transacciones
        TransactionService.create_transaction(
            db=db_session,
            user_id=test_user.id,
            account_id=test_account.id,
            transaction_type="income",
            amount=3000.00,
            category="salary",
            description="Monthly salary",
            transaction_date=date.today()
        )
        
        TransactionService.create_transaction(
            db=db_session,
            user_id=test_user.id,
            account_id=test_account.id,
            transaction_type="expense",
            amount=1500.00,
            category="rent",
            description="Monthly rent",
            transaction_date=date.today()
        )
        
        metrics = AnalyticsService.calculate_monthly_metrics(
            db_session,
            test_user.id
        )
        assert "total_income" in metrics
        assert "total_expenses" in metrics
        assert metrics["total_income"] >= 3000.00
        assert metrics["total_expenses"] >= 1500.00

    def test_get_financial_overview(self, db_session, test_user, test_account):
        """Prueba obtener overview financiero"""
        overview = AnalyticsService.get_financial_overview(
            db_session,
            test_user.id
        )
        assert "total_balance" in overview
        assert "accounts_count" in overview
        assert overview["total_balance"] >= test_account.current_balance

    def test_calculate_savings_rate(self, db_session):
        """Prueba calcular tasa de ahorro"""
        income = 5000.00
        expenses = 3000.00
        savings_rate = AnalyticsService.calculate_savings_rate(income, expenses)
        assert savings_rate == 40.0  # (5000 - 3000) / 5000 * 100

    def test_calculate_savings_rate_zero_income(self, db_session):
        """Prueba calcular tasa de ahorro con ingreso cero"""
        savings_rate = AnalyticsService.calculate_savings_rate(0, 0)
        assert savings_rate == 0.0
