# 📚 Arquitectura del Backend - Guía Resumida

## 🏗️ Estructura General

El backend está construido con **FastAPI** (framework web moderno de Python) y sigue una arquitectura de **capas separadas** para mejor organización.

```
backend/
├── main.py              # Punto de entrada - Define todos los endpoints de la API
├── models.py            # Modelos de base de datos (tablas)
├── schemas.py           # Esquemas de validación (entrada/salida de datos)
├── services.py          # Lógica de negocio (operaciones complejas)
├── database.py          # Configuración de conexión a la base de datos
├── auth.py              # Sistema de autenticación (login, tokens)
└── requirements.txt     # Lista de dependencias de Python
```

---

## 📦 Archivos Principales

### 1️⃣ **`main.py` - Servidor y Endpoints**

**¿Qué hace?**
- Es el corazón del backend
- Define todos los "puntos de acceso" (endpoints) que el frontend puede llamar
- Maneja las peticiones HTTP (GET, POST, PUT, DELETE)

**Endpoints principales:**
```python
# Autenticación
POST /api/auth/register    # Registrar nuevo usuario
POST /api/auth/login       # Iniciar sesión (devuelve token)
GET  /api/auth/me          # Obtener datos del usuario actual

# Plataformas
GET  /api/platforms        # Listar todas las plataformas disponibles
POST /api/platforms        # Crear nueva plataforma

# Cuentas
GET  /api/accounts         # Obtener todas las cuentas del usuario
POST /api/accounts         # Crear nueva cuenta
PUT  /api/accounts/{id}    # Actualizar cuenta
DELETE /api/accounts/{id}  # Eliminar cuenta

# Transacciones
GET  /api/transactions     # Obtener transacciones del usuario
POST /api/transactions     # Crear nueva transacción
PUT  /api/transactions/{id}   # Actualizar transacción
DELETE /api/transactions/{id} # Eliminar transacción

# Objetivos Financieros
GET  /api/goals            # Obtener objetivos del usuario
POST /api/goals            # Crear nuevo objetivo
PUT  /api/goals/{id}       # Actualizar objetivo
DELETE /api/goals/{id}     # Eliminar objetivo

# Analytics
GET  /api/analytics/overview     # Resumen financiero general
GET  /api/analytics/metrics      # Métricas del mes específico

# AI Assistant
POST /api/ai/advice        # Obtener consejo financiero de IA
```

**Conceptos clave:**
- `Depends(get_current_active_user)`: Solo usuarios autenticados pueden acceder
- `response_model`: Define qué formato de datos se devuelve
- `Session = Depends(get_db)`: Conexión a la base de datos

---

### 2️⃣ **`models.py` - Base de Datos (Tablas)**

**¿Qué hace?**
- Define la estructura de las tablas en la base de datos
- Cada clase = una tabla

**Tablas principales:**

```python
# Usuario
class User:
    - id (único)
    - email
    - password_hash (encriptado)
    - full_name
    - fecha de creación
    
# Plataforma (ej: Nequi, Bancolombia, Davivienda)
class Platform:
    - id
    - name
    - platform_type (bank, fintech, wallet)
    - icono
    
# Cuenta Bancaria
class Account:
    - id
    - user_id (dueño)
    - platform_id (a qué plataforma pertenece)
    - account_name
    - account_type (checking, savings, investment, credit)
    - current_balance (saldo actual)
    
# Transacción
class Transaction:
    - id
    - user_id
    - account_id
    - transaction_type (income, expense)
    - amount (monto)
    - category (categoría: Food, Transport, etc.)
    - description
    - transaction_date
    
# Objetivo Financiero
class FinancialGoal:
    - id
    - user_id
    - goal_name
    - goal_type (savings, debt_reduction, investment)
    - target_amount (meta)
    - current_amount (progreso actual)
    - target_date
    - priority (high, medium, low)
    - is_active
```

**Relaciones:**
- Un **Usuario** puede tener muchas **Cuentas**
- Una **Cuenta** pertenece a una **Plataforma**
- Una **Cuenta** puede tener muchas **Transacciones**
- Un **Usuario** puede tener muchos **Objetivos**

---

### 3️⃣ **`schemas.py` - Validación de Datos**

**¿Qué hace?**
- Define QUÉ datos son válidos para entrar y salir del sistema
- Valida tipos de datos, formatos, campos requeridos

**Ejemplo:**
```python
# Para crear una cuenta
class AccountCreate:
    account_name: str          # obligatorio
    platform_id: int           # obligatorio
    account_type: str          # obligatorio
    current_balance: float     # obligatorio

# Al devolver una cuenta (incluye más info)
class Account:
    id: int                    # lo agrega la BD
    account_name: str
    platform_id: int
    account_type: str
    current_balance: float
    created_at: datetime       # fecha de creación
    platform: Platform         # datos completos de la plataforma
```

**¿Por qué es útil?**
- Evita errores (ej: enviar texto donde debe ir un número)
- Documenta automáticamente la API
- Convierte datos automáticamente

---

### 4️⃣ **`services.py` - Lógica de Negocio**

**¿Qué hace?**
- Contiene la lógica compleja de la aplicación
- Operaciones que involucran múltiples tablas
- Cálculos y análisis

**Servicios principales:**

#### **PlatformService**
```python
- create_platform()        # Crea nueva plataforma
- get_all_platforms()      # Lista todas las plataformas
```

#### **AccountService**
```python
- create_account()         # Crea cuenta nueva
- get_user_accounts()      # Obtiene cuentas del usuario
- update_account()         # Actualiza saldo/info de cuenta
- delete_account()         # Elimina cuenta
```

#### **TransactionService**
```python
- create_transaction()     # Crea transacción
- get_user_transactions()  # Obtiene transacciones
- update_transaction()     # Modifica transacción
- delete_transaction()     # Elimina transacción
```

#### **FinancialGoalService**
```python
- create_goal()            # Crea objetivo financiero
- get_user_goals()         # Obtiene objetivos del usuario
- update_goal()            # Actualiza progreso/meta
- delete_goal()            # Elimina objetivo
```

#### **FinancialAnalyticsService** (el más complejo)
```python
- get_financial_overview()
  * Calcula balance total de todas las cuentas
  * Suma ingresos del mes
  * Suma gastos del mes
  * Calcula tasa de ahorro
  * Resume cuentas por plataforma
  * Últimas transacciones
  * Objetivos activos

- calculate_monthly_metrics()
  * Métricas específicas de un mes/año
  * Ingresos del mes
  * Gastos del mes
  * Tasa de ahorro del mes
```

#### **AIAssistantService**
```python
- get_financial_advice()
  * Obtiene contexto financiero del usuario
  * Si tiene API key de OpenAI: usa GPT-3.5
  * Si no: usa respuestas basadas en reglas
  * Genera recomendaciones personalizadas
```

---

### 5️⃣ **`database.py` - Configuración de BD**

**¿Qué hace?**
- Configura la conexión a SQLite
- Crea la base de datos si no existe
- Proporciona sesiones de BD a los endpoints

**Componentes:**
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"
engine = create_engine(...)     # Motor de BD
SessionLocal = sessionmaker()   # Fábrica de sesiones
Base = declarative_base()       # Base para modelos
```

---

### 6️⃣ **`auth.py` - Autenticación y Seguridad**

**¿Qué hace?**
- Maneja login y registro de usuarios
- Crea y valida tokens JWT (para mantener sesión)
- Encripta contraseñas

**Funciones principales:**
```python
- verify_password()          # Verifica si contraseña es correcta
- get_password_hash()        # Encripta contraseña
- create_access_token()      # Crea token de sesión (JWT)
- get_current_user()         # Obtiene usuario del token
- get_current_active_user()  # Verifica que usuario esté activo
```

**Flujo de autenticación:**
1. Usuario se registra → contraseña se encripta y guarda
2. Usuario hace login → verifica contraseña → crea token JWT
3. Usuario hace peticiones → envía token → backend verifica token
4. Si token es válido → permite acceso, si no → error 401

**Seguridad:**
- Contraseñas hasheadas con bcrypt (imposible descifrar)
- Tokens JWT firmados (no se pueden falsificar)
- Tokens expiran en 30 minutos

---

## 🔄 Flujo de una Petición Típica

### Ejemplo: Crear una transacción

1. **Frontend** envía:
```javascript
POST /api/transactions
{
  "account_id": 1,
  "transaction_type": "expense",
  "amount": 50.00,
  "category": "Food & Dining",
  "description": "Almuerzo",
  "transaction_date": "2025-10-12"
}
```

2. **main.py** recibe la petición
   - Verifica token de autenticación
   - Obtiene usuario actual

3. **schemas.py** valida los datos
   - Verifica que todos los campos estén presentes
   - Verifica tipos de datos correctos

4. **services.py** ejecuta la lógica
   - Crea la transacción en la BD
   - Actualiza el balance de la cuenta

5. **Backend** responde:
```json
{
  "id": 123,
  "account_id": 1,
  "transaction_type": "expense",
  "amount": 50.00,
  "category": "Food & Dining",
  "description": "Almuerzo",
  "transaction_date": "2025-10-12T00:00:00",
  "created_at": "2025-10-12T13:45:00"
}
```

---

## 🗄️ Base de Datos

**Tecnología:** SQLite (archivo `finance.db`)

**¿Por qué SQLite?**
- ✅ No requiere servidor separado
- ✅ Perfecto para desarrollo y apps personales
- ✅ Fácil de migrar a PostgreSQL/MySQL después

**Ubicación:** `backend/finance.db`

---

## 🔐 Seguridad Implementada

1. **Contraseñas encriptadas** (bcrypt)
2. **Tokens JWT** para autenticación
3. **Validación de datos** en todos los endpoints
4. **CORS configurado** (solo frontend permitido)
5. **Usuarios autenticados** requeridos en endpoints sensibles

---

## 📊 Tecnologías Clave

- **FastAPI**: Framework web rápido y moderno
- **SQLAlchemy**: ORM para manejar base de datos
- **Pydantic**: Validación de datos
- **bcrypt**: Encriptación de contraseñas
- **JWT**: Tokens de autenticación
- **Uvicorn**: Servidor ASGI para correr FastAPI
- **OpenAI (opcional)**: API de inteligencia artificial
