import pytest
from fastapi import status
from datetime import date, timedelta


class TestTransactions:
    """Pruebas para el módulo de transacciones"""

    def test_create_income_transaction(self, client, auth_headers, test_account):
        """Prueba crear transacción de ingreso"""
        initial_balance = test_account.current_balance
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": 500.00,
                "category": "salary",
                "description": "Monthly salary",
                "transaction_date": str(date.today())
            }
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["transaction_type"] == "income"
        assert data["amount"] == 500.00
        assert data["category"] == "salary"

    def test_create_expense_transaction(self, client, auth_headers, test_account):
        """Prueba crear transacción de gasto"""
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "expense",
                "amount": 150.00,
                "category": "groceries",
                "description": "Weekly groceries",
                "transaction_date": str(date.today())
            }
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["transaction_type"] == "expense"
        assert data["amount"] == 150.00

    def test_create_expense_insufficient_balance(self, client, auth_headers, test_account):
        """Prueba crear gasto con balance insuficiente"""
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "expense",
                "amount": 10000.00,  # Más del balance disponible
                "category": "entertainment",
                "description": "Too expensive",
                "transaction_date": str(date.today())
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "insufficient" in response.json()["detail"].lower()

    def test_create_transaction_future_date(self, client, auth_headers, test_account):
        """Prueba crear transacción con fecha futura"""
        future_date = date.today() + timedelta(days=30)
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": 100.00,
                "category": "other",
                "description": "Future transaction",
                "transaction_date": str(future_date)
            }
        )
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            assert "future" in response.json()["detail"].lower()

    def test_create_transaction_negative_amount(self, client, auth_headers, test_account):
        """Prueba crear transacción con monto negativo"""
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": -100.00,
                "category": "other",
                "description": "Negative amount",
                "transaction_date": str(date.today())
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_user_transactions(self, client, auth_headers, test_account):
        """Prueba obtener transacciones del usuario"""
        # Crear algunas transacciones
        client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": 100.00,
                "category": "salary",
                "description": "Test income",
                "transaction_date": str(date.today())
            }
        )
        
        response = client.get("/api/transactions", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_transactions_by_account(self, client, auth_headers, test_account):
        """Prueba obtener transacciones por cuenta específica"""
        response = client.get(
            f"/api/transactions?account_id={test_account.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_transactions_by_type(self, client, auth_headers, test_account):
        """Prueba filtrar transacciones por tipo"""
        # Crear transacción de ingreso
        client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": 200.00,
                "category": "salary",
                "description": "Income test",
                "transaction_date": str(date.today())
            }
        )
        
        response = client.get(
            "/api/transactions?transaction_type=income",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for transaction in data:
            assert transaction["transaction_type"] == "income"

    def test_get_transactions_by_date_range(self, client, auth_headers, test_account):
        """Prueba filtrar transacciones por rango de fechas"""
        start_date = date.today() - timedelta(days=7)
        end_date = date.today()
        
        response = client.get(
            f"/api/transactions?start_date={start_date}&end_date={end_date}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_delete_transaction(self, client, auth_headers, test_account):
        """Prueba eliminar transacción"""
        # Crear transacción
        create_response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": test_account.id,
                "transaction_type": "income",
                "amount": 50.00,
                "category": "other",
                "description": "To be deleted",
                "transaction_date": str(date.today())
            }
        )
        transaction_id = create_response.json()["id"]
        
        # Eliminar transacción
        response = client.delete(
            f"/api/transactions/{transaction_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create_transaction_account_not_owned(self, client, auth_headers, db_session, test_platform):
        """Prueba crear transacción en cuenta que no pertenece al usuario"""
        from database import User, Account
        from auth import get_password_hash
        from datetime import datetime
        
        # Crear otro usuario y su cuenta
        other_user = User(
            email="other@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Other User",
            is_active=True,
            created_at=datetime.utcnow()
        )
        db_session.add(other_user)
        db_session.commit()
        
        other_account = Account(
            user_id=other_user.id,
            platform_id=test_platform.id,
            account_name="Other Account",
            account_type="checking",
            account_number="OTHER456",
            current_balance=1000.00,
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow()
        )
        db_session.add(other_account)
        db_session.commit()
        
        # Intentar crear transacción
        response = client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "account_id": other_account.id,
                "transaction_type": "income",
                "amount": 100.00,
                "category": "other",
                "description": "Unauthorized transaction",
                "transaction_date": str(date.today())
            }
        )
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
