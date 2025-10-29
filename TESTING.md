# Documentación de Pruebas - FinanceApp

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Backend - Pruebas Python](#backend---pruebas-python)
3. [Frontend - Pruebas Vue.js](#frontend---pruebas-vuejs)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Cobertura de Código](#cobertura-de-código)
6. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

Este proyecto implementa pruebas unitarias completas tanto para el backend (FastAPI) como para el frontend (Vue.js 3), siguiendo las mejores prácticas de DevOps y desarrollo ágil.

### Objetivos de las Pruebas
- ✅ Garantizar la calidad del código
- ✅ Prevenir regresiones
- ✅ Facilitar el mantenimiento
- ✅ Documentar el comportamiento esperado
- ✅ Acelerar el desarrollo con confianza

---

## Backend - Pruebas Python

### Tecnologías Utilizadas
- **pytest**: Framework de pruebas
- **pytest-cov**: Cobertura de código
- **httpx**: Cliente HTTP para pruebas de API
- **FastAPI TestClient**: Cliente de pruebas para FastAPI

### Estructura de Pruebas

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Configuración y fixtures
│   ├── test_auth.py          # Pruebas de autenticación
│   ├── test_accounts.py      # Pruebas de cuentas
│   ├── test_transactions.py  # Pruebas de transacciones
│   └── test_services.py      # Pruebas de servicios
└── requirements-test.txt     # Dependencias de pruebas
```

### Ejecutar Pruebas

```bash
# Navegar al directorio backend
cd backend

# Instalar dependencias
pip install -r requirements.txt -r requirements-test.txt

# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=. --cov-report=html

# Ejecutar pruebas específicas
pytest tests/test_auth.py
pytest tests/test_auth.py::TestAuthentication::test_login_success

# Modo verbose
pytest -v

# Ver print statements
pytest -s
```

### Cobertura Esperada
- **Meta**: 80% de cobertura mínima
- **Áreas críticas**: 100% (auth, transacciones)

### Ejemplos de Pruebas

#### Prueba de Autenticación
```python
def test_login_success(client, test_user):
    """Prueba login exitoso"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

#### Prueba de Transacción
```python
def test_create_expense_insufficient_balance(client, auth_headers, test_account):
    """Prueba crear gasto con balance insuficiente"""
    response = client.post(
        "/api/transactions",
        headers=auth_headers,
        json={
            "account_id": test_account.id,
            "transaction_type": "expense",
            "amount": 10000.00,
            "category": "entertainment",
            "description": "Too expensive",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()
```

---

## Frontend - Pruebas Vue.js

### Tecnologías Utilizadas
- **Vitest**: Framework de pruebas rápido
- **Vue Test Utils**: Utilidades para probar componentes Vue
- **jsdom**: Simulación de DOM
- **@vitest/ui**: Interfaz gráfica para pruebas

### Estructura de Pruebas

```
frontend/
├── src/
│   └── tests/
│       ├── setup.js              # Configuración global
│       ├── stores/
│       │   ├── auth.spec.js      # Pruebas de auth store
│       │   ├── finance.spec.js   # Pruebas de finance store
│       │   └── theme.spec.js     # Pruebas de theme store
│       └── views/
│           ├── Login.spec.js     # Pruebas de Login
│           └── Dashboard.spec.js # Pruebas de Dashboard
└── vitest.config.js              # Configuración de Vitest
```

### Ejecutar Pruebas

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar todas las pruebas
npm test

# Ejecutar con interfaz gráfica
npm run test:ui

# Ejecutar con cobertura
npm run test:coverage

# Modo watch (re-ejecuta en cambios)
npm test -- --watch

# Ejecutar prueba específica
npm test -- auth.spec.js
```

### Ejemplos de Pruebas

#### Prueba de Store (Pinia)
```javascript
describe('Auth Store', () => {
  it('debe hacer login exitosamente', async () => {
    const store = useAuthStore()
    const mockResponse = {
      data: {
        access_token: 'test-token-123',
        token_type: 'bearer'
      }
    }
    
    axios.post.mockResolvedValueOnce(mockResponse)
    await store.login('test@example.com', 'password123')

    expect(store.token).toBe('test-token-123')
    expect(store.isAuthenticated).toBe(true)
  })
})
```

#### Prueba de Componente
```javascript
describe('Login View', () => {
  it('renderiza el formulario de login', () => {
    const wrapper = mount(Login)
    
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
  })
})
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

El proyecto incluye un pipeline de CI/CD completo que se ejecuta automáticamente en cada push o pull request.

#### Jobs del Pipeline

1. **test-backend**
   - Instala Python y dependencias
   - Ejecuta pytest con cobertura
   - Sube resultados a Codecov

2. **test-frontend**
   - Instala Node.js y dependencias
   - Ejecuta Vitest con cobertura
   - Sube resultados a Codecov

3. **lint-backend**
   - Ejecuta flake8 para verificar estilo de código

4. **build-backend**
   - Construye imagen Docker del backend
   - Sube a Docker Hub (solo en main)

5. **build-frontend**
   - Construye el frontend para producción
   - Genera artefactos

6. **deploy**
   - Despliega la aplicación (configurar según plataforma)

7. **notify**
   - Envía notificaciones del resultado

### Configuración de Secrets

Para que el pipeline funcione completamente, configura estos secrets en GitHub:

1. **DOCKERHUB_USERNAME**: Tu usuario de Docker Hub
2. **DOCKERHUB_TOKEN**: Token de acceso de Docker Hub
3. **CODECOV_TOKEN**: Token de Codecov (opcional)

```bash
# En tu repositorio de GitHub:
# Settings → Secrets and variables → Actions → New repository secret
```

### Estado del Pipeline

Ver el estado en: `https://github.com/tu-usuario/FinanceApp/actions`

---

## Cobertura de Código

### Backend

```bash
# Generar reporte HTML
cd backend
pytest --cov=. --cov-report=html
# Abrir: backend/htmlcov/index.html

# Generar reporte en terminal
pytest --cov=. --cov-report=term-missing
```

### Frontend

```bash
# Generar reporte HTML
cd frontend
npm run test:coverage
# Abrir: frontend/coverage/index.html
```

### Métricas de Cobertura

| Módulo | Cobertura Mínima | Cobertura Actual |
|--------|------------------|------------------|
| Backend - Auth | 90% | ✅ |
| Backend - Services | 80% | ✅ |
| Backend - Models | 70% | ✅ |
| Frontend - Stores | 85% | ✅ |
| Frontend - Views | 75% | ✅ |

---

## Mejores Prácticas

### Escritura de Pruebas

1. **AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_example():
       # Arrange: Preparar datos
       user = create_test_user()
       
       # Act: Ejecutar acción
       result = login(user)
       
       # Assert: Verificar resultado
       assert result.success is True
   ```

2. **Nombres Descriptivos**
   ```python
   # ❌ Mal
   def test_1():
       ...
   
   # ✅ Bien
   def test_user_login_with_valid_credentials_returns_token():
       ...
   ```

3. **Una Aserción por Prueba** (cuando sea posible)
   ```python
   # ✅ Enfocado
   def test_user_email_is_saved():
       user = create_user(email="test@example.com")
       assert user.email == "test@example.com"
   ```

4. **Independencia de Pruebas**
   - Cada prueba debe poder ejecutarse de forma independiente
   - No depender del orden de ejecución
   - Limpiar estado después de cada prueba

5. **Mocks y Stubs**
   ```python
   # Mock de API externa
   @patch('services.OpenAI')
   def test_ai_advice(mock_openai):
       mock_openai.return_value.complete.return_value = "advice"
       result = get_ai_advice()
       assert result == "advice"
   ```

### Testing Pyramid

```
    /\
   /  \    E2E Tests (10%)
  /____\   Integration Tests (30%)
 /______\  Unit Tests (60%)
```

### Comandos Útiles

```bash
# Backend
pytest -v                          # Verbose
pytest -k "auth"                   # Solo pruebas con "auth" en nombre
pytest --lf                        # Solo pruebas que fallaron
pytest --maxfail=1                 # Detener después de 1 fallo
pytest -x                          # Detener en primer fallo

# Frontend
npm test -- --reporter=verbose    # Verbose
npm test -- --ui                  # Interfaz gráfica
npm test -- --coverage            # Con cobertura
npm test -- auth                  # Solo pruebas de auth
```

---

## Troubleshooting

### Problemas Comunes

#### Backend

**Error: ModuleNotFoundError**
```bash
# Solución: Instalar dependencias
pip install -r requirements.txt -r requirements-test.txt
```

**Error: Database locked**
```bash
# Solución: Las pruebas usan SQLite en memoria, verificar conftest.py
```

#### Frontend

**Error: Cannot find module '@/...'**
```bash
# Solución: Verificar alias en vitest.config.js
```

**Error: ReferenceError: localStorage is not defined**
```bash
# Solución: Verificar setup.js con el mock de localStorage
```

---

## Contribuir

### Agregar Nuevas Pruebas

1. **Backend**:
   - Crear archivo `test_*.py` en `backend/tests/`
   - Usar fixtures de `conftest.py`
   - Seguir patrón AAA

2. **Frontend**:
   - Crear archivo `*.spec.js` en `frontend/src/tests/`
   - Usar Vue Test Utils para componentes
   - Usar Pinia para stores

### Pull Request Checklist

- [ ] Todas las pruebas pasan localmente
- [ ] Cobertura no disminuye
- [ ] Pruebas para nuevas funcionalidades
- [ ] Nombres descriptivos
- [ ] Sin pruebas comentadas/deshabilitadas

---

## Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## Contacto

Para preguntas o problemas con las pruebas, abre un issue en GitHub o contacta al equipo de desarrollo.

**¡Feliz testing! 🧪✨**
