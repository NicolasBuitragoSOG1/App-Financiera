import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Account, Transaction, FinancialGoal, BankingPlatform
from auth import get_password_hash

# Base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Sobrescribe la dependencia de base de datos para usar la BD de pruebas"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Crea una sesión de base de datos limpia para cada prueba"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de prueba de FastAPI"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Usuario de prueba"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_platform(db_session):
    """Plataforma bancaria de prueba"""
    platform = BankingPlatform(
        name="Test Bank",
        platform_type="bank",
        logo_url="https://example.com/logo.png"
    )
    db_session.add(platform)
    db_session.commit()
    db_session.refresh(platform)
    return platform


@pytest.fixture
def test_account(db_session, test_user, test_platform):
    """Cuenta bancaria de prueba"""
    account = Account(
        user_id=test_user.id,
        platform_id=test_platform.id,
        account_name="Test Account",
        account_type="checking",
        current_balance=1000.00,
        currency="USD"
    )
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)
    return account


@pytest.fixture
def auth_headers(client, test_user):
    """Headers de autenticación para pruebas"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
