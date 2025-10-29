import pytest
from fastapi import status


class TestAccounts:
    """Pruebas para el módulo de cuentas bancarias"""

    def test_create_account_success(self, client, auth_headers, test_platform):
        """Prueba creación exitosa de cuenta"""
        response = client.post(
            "/api/accounts",
            headers=auth_headers,
            json={
                "platform_id": test_platform.id,
                "account_name": "Savings Account",
                "account_type": "savings",
                "account_number": "1234567890",
                "current_balance": 5000.00,
                "currency": "USD"
            }
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["account_name"] == "Savings Account"
        assert data["account_type"] == "savings"
        assert data["current_balance"] == 5000.00
        assert data["currency"] == "USD"

    def test_create_account_invalid_platform(self, client, auth_headers):
        """Prueba creación de cuenta con plataforma inexistente"""
        response = client.post(
            "/api/accounts",
            headers=auth_headers,
            json={
                "platform_id": 99999,
                "account_name": "Test Account",
                "account_type": "checking",
                "account_number": "9999999999",
                "current_balance": 1000.00,
                "currency": "USD"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_accounts(self, client, auth_headers, test_account):
        """Prueba obtener cuentas del usuario"""
        response = client.get("/api/accounts", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == test_account.id

    def test_get_user_accounts_without_auth(self, client):
        """Prueba obtener cuentas sin autenticación"""
        response = client.get("/api/accounts")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_account_by_id(self, client, auth_headers, test_account):
        """Prueba obtener cuenta específica por ID"""
        response = client.get(
            f"/api/accounts/{test_account.id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_account.id
        assert data["account_name"] == test_account.account_name

    def test_get_account_not_found(self, client, auth_headers):
        """Prueba obtener cuenta inexistente"""
        response = client.get("/api/accounts/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_account_balance(self, client, auth_headers, test_account):
        """Prueba actualizar balance de cuenta"""
        new_balance = 2500.00
        response = client.patch(
            f"/api/accounts/{test_account.id}",
            headers=auth_headers,
            json={"current_balance": new_balance}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["current_balance"] == new_balance

    def test_delete_account(self, client, auth_headers, test_account):
        """Prueba eliminar cuenta"""
        account_id = test_account.id
        response = client.delete(
            f"/api/accounts/{account_id}",
            headers=auth_headers
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

    def test_delete_account_not_owned(self, client, auth_headers, db_session, test_platform):
        """Prueba eliminar cuenta que no pertenece al usuario"""
        # Crear otro usuario y su cuenta
        from database import User, Account
        from auth import get_password_hash
        from datetime import datetime
        
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
            account_number="OTHER123",
            current_balance=1000.00,
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow()
        )
        db_session.add(other_account)
        db_session.commit()
        
        # Intentar eliminar con otro usuario
        response = client.delete(
            f"/api/accounts/{other_account.id}",
            headers=auth_headers
        )
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
