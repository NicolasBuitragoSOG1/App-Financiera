# Finance Manager - Documentación Completa

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura General](#arquitectura-general)
3. [Características Principales](#características-principales)
4. [Cómo Funciona la Aplicación](#cómo-funciona-la-aplicación)
5. [Flujo de Datos](#flujo-de-datos)
6. [Tecnologías Utilizadas](#tecnologías-utilizadas)
7. [Instalación y Configuración](#instalación-y-configuración)
8. [Estructura de Archivos](#estructura-de-archivos)

---

## Visión General

**Finance Manager** es una aplicación web para gestión de finanzas personales que permite:
- Administrar múltiples cuentas bancarias
- Registrar y categorizar transacciones (ingresos y gastos)
- Establecer y dar seguimiento a objetivos financieros
- Visualizar análisis financieros con gráficos
- Recibir consejos financieros personalizados de un asistente de IA
- Modo oscuro completo

**Tipo de aplicación:** Full-stack web application (SPA - Single Page Application)

---

## Arquitectura General

La aplicación sigue una arquitectura **Cliente-Servidor** con separación completa entre frontend y backend:

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIO                               │
│                    (Navegador Web)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    FRONTEND                                  │
│                    Vue.js 3                                  │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Views     │  │    Stores    │  │   Router     │      │
│  │  (Páginas)  │  │   (Pinia)    │  │(Navegación)  │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  Componentes: Dashboard, Accounts, Transactions, Goals,     │
│               Analytics, AI Assistant                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API (JSON)
                     │ Endpoints: /api/*
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    BACKEND                                   │
│                   FastAPI (Python)                           │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Endpoints  │  │   Services   │  │    Models    │      │
│  │   (main)    │  │   (Lógica)   │  │     (BD)     │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  Seguridad: JWT Authentication, Password Hashing            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ SQL Queries
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 BASE DE DATOS                                │
│                  SQLite (finance.db)                         │
│                                                              │
│  Tablas: users, platforms, accounts, transactions, goals    │
└──────────────────────────────────────────────────────────────┘
```

---

## Características Principales

### 1. **Gestión de Usuarios y Autenticación**
- Registro de nuevos usuarios
- Inicio de sesión con email y contraseña
- Sesiones seguras con tokens JWT
- Encriptación de contraseñas con bcrypt

### 2. **Gestión de Cuentas Bancarias**
- Crear cuentas en múltiples plataformas (bancos, fintechs, wallets)
- Tipos de cuenta: Checking, Savings, Investment, Credit
- Ver balance total de todas las cuentas
- Actualizar balances
- Eliminar cuentas

### 3. **Registro de Transacciones**
- Registrar ingresos y gastos
- Categorización automática (Food, Transport, Bills, etc.)
- Filtrado por tipo, categoría y cuenta
- Tabla ordenada cronológicamente
- Editar y eliminar transacciones

### 4. **Objetivos Financieros**
- Crear objetivos de ahorro, inversión o reducción de deuda
- Establecer metas con fecha límite
- Dar seguimiento al progreso con barras visuales
- Priorizar objetivos (High, Medium, Low)
- Actualizar progreso fácilmente

### 5. **Analytics y Reportes**
- Dashboard con resumen financiero
- Gráficos interactivos (Chart.js):
  - Barras: Ingresos vs Gastos
  - Dona: Distribución de gastos por categoría
- Métricas mensuales:
  - Tasa de ahorro
  - Ingreso neto
  - Promedio de gasto diario
- Financial Health Score (0-100)
- Recomendaciones personalizadas

### 6. **AI Financial Assistant**
- Chat inteligente con contexto financiero
- Respuestas personalizadas basadas en tus datos reales
- Integración opcional con OpenAI GPT-3.5
- Sistema de fallback con respuestas basadas en reglas
- Detección automática de idioma (inglés/español)

### 7. **Modo Oscuro Completo**
- Toggle de tema claro/oscuro
- Persistencia de preferencia en localStorage
- Adaptación de todos los componentes
- Gráficos adaptativos con colores optimizados

---

## Cómo Funciona la Aplicación

### Flujo de Usuario Típico:

#### 1. **Registro e Inicio de Sesión**
```
Usuario → Registro → Backend valida → Crea usuario → 
Backend hashea contraseña → Guarda en BD → Responde éxito → 
Usuario hace login → Backend verifica → Crea token JWT → 
Frontend guarda token → Redirige a Dashboard
```

#### 2. **Agregar una Cuenta**
```
Dashboard → Click "Add Account" → Modal se abre → 
Usuario llena formulario → Submit → 
Frontend valida → Envía a /api/accounts → 
Backend crea cuenta en BD → Responde con cuenta creada → 
Frontend actualiza lista → Modal se cierra → 
Cuenta aparece en dashboard
```

#### 3. **Registrar una Transacción**
```
Transactions → Click "Add Transaction" → Modal se abre → 
Usuario selecciona cuenta, tipo, categoría, monto → Submit → 
Frontend envía a /api/transactions → 
Backend crea transacción → Actualiza balance de cuenta → 
Responde con transacción creada → 
Frontend actualiza tabla y balance → Modal se cierra
```

#### 4. **Ver Analytics**
```
Analytics → Selecciona mes/año → Click "Analyze" → 
Frontend pide métricas al backend → 
Backend calcula ingresos, gastos, tasa de ahorro → 
Agrupa transacciones por categoría → Responde JSON → 
Frontend recibe datos → Crea gráficos con Chart.js → 
Muestra visualizaciones
```

#### 5. **Usar AI Assistant**
```
AI Assistant → Usuario escribe pregunta → Submit → 
Frontend agrega mensaje al chat → Muestra "thinking..." → 
Envía query a /api/ai/advice → 
Backend obtiene contexto financiero del usuario → 
Si tiene OpenAI key: llama GPT-3.5 → 
Si no: usa sistema basado en reglas → 
Genera recomendaciones → Responde → 
Frontend agrega respuesta al chat → Scroll al final
```

---

## Flujo de Datos Detallado

### Ejemplo: Crear un Objetivo Financiero

```
┌──────────────┐
│   USUARIO    │ "Quiero ahorrar $500 para vacaciones"
└──────┬───────┘
       │
       │ 1. Click "Create Goal"
       ▼
┌──────────────────────────┐
│  Goals.vue (Vista)       │
│                          │
│  showCreateModal = true  │ Abre modal
└──────┬───────────────────┘
       │
       │ 2. Llena formulario:
       │    - Goal Name: "Vacation Fund"
       │    - Type: "savings"
       │    - Target: $500
       │    - Date: 2025-12-31
       │
       │ 3. Click "Create"
       ▼
┌────────────────────────────┐
│  createGoal() función      │
│                            │
│  Valida datos localmente   │
└──────┬─────────────────────┘
       │
       │ 4. Llama al store
       ▼
┌────────────────────────────────┐
│  financeStore.createGoal()     │
│                                │
│  await axios.post(             │
│    '/api/goals',               │
│    goalData                    │
│  )                             │
└──────┬─────────────────────────┘
       │
       │ 5. HTTP POST con token JWT
       │    Authorization: Bearer <token>
       ▼
┌──────────────────────────────────────┐
│  BACKEND - main.py                   │
│                                      │
│  @app.post("/api/goals")             │
│  - Verifica token                    │
│  - Obtiene user_id del token         │
│  - Valida datos con schema           │
└──────┬───────────────────────────────┘
       │
       │ 6. Llama al servicio
       ▼
┌──────────────────────────────────────┐
│  FinancialGoalService.create_goal()  │
│                                      │
│  - Crea objeto Goal                  │
│  - goal.user_id = current_user_id    │
│  - goal.is_active = True             │
│  - db.add(goal)                      │
│  - db.commit()                       │
│  - db.refresh(goal)                  │
└──────┬───────────────────────────────┘
       │
       │ 7. Inserta en BD
       ▼
┌──────────────────────────────┐
│  SQLite - finance.db         │
│                              │
│  INSERT INTO financial_goals │
│  VALUES (...)                │
│                              │
│  Retorna: id=15 (nuevo)      │
└──────┬───────────────────────┘
       │
       │ 8. Respuesta exitosa
       ▼
┌──────────────────────────────────────┐
│  Backend responde JSON:              │
│  {                                   │
│    "id": 15,                         │
│    "goal_name": "Vacation Fund",     │
│    "goal_type": "savings",           │
│    "target_amount": 500.00,          │
│    "current_amount": 0.00,           │
│    "target_date": "2025-12-31",      │
│    "priority": "medium",             │
│    "is_active": true,                │
│    "user_id": 1                      │
│  }                                   │
└──────┬───────────────────────────────┘
       │
       │ 9. Frontend recibe respuesta
       ▼
┌────────────────────────────────┐
│  financeStore                  │
│                                │
│  this.goals.push(newGoal)      │ Agrega a la lista
└──────┬─────────────────────────┘
       │
       │ 10. Vue detecta cambio (reactive)
       ▼
┌────────────────────────────────┐
│  Goals.vue actualiza UI        │
│                                │
│  - Cierra modal                │
│  - Nueva tarjeta aparece       │
│  - Muestra toast de éxito      │
└────────────────────────────────┘
```

---

## Tecnologías Utilizadas

### **Backend:**
| Tecnología | Propósito | Por qué |
|-----------|-----------|---------|
| Python 3.x | Lenguaje base | Popular, fácil de leer, gran ecosistema |
| FastAPI | Framework web | Rápido, moderno, auto-documentación |
| SQLAlchemy | ORM | Abstrae SQL, facilita migraciones |
| Pydantic | Validación | Valida datos automáticamente |
| JWT | Autenticación | Stateless, seguro, escalable |
| bcrypt | Hash de passwords | Estándar de seguridad |
| OpenAI | IA (opcional) | GPT-3.5 para consejos inteligentes |
| Uvicorn | Servidor ASGI | Rápido, compatible con async |
| SQLite | Base de datos | Ligera, sin servidor, perfecta para dev |

### **Frontend:**
| Tecnología | Propósito | Por qué |
|-----------|-----------|---------|
| Vue.js 3 | Framework JS | Reactivo, componentes, fácil de aprender |
| Pinia | State management | Moderno, TypeScript, más simple que Vuex |
| Vue Router | Navegación | SPA routing, guards de autenticación |
| Axios | Cliente HTTP | Promesas, interceptors, fácil configuración |
| Tailwind CSS | Estilos | Utility-first, rápido, customizable |
| Chart.js | Gráficos | Simple, interactivo, responsive |
| Heroicons | Iconos | SVG, tree-shakeable, diseño consistente |
| Vue Toastification | Notificaciones | Toast messages, customizable |
| date-fns | Fechas | Moderna, modular, sin mutaciones |
| Vite | Build tool | Ultra-rápido, HMR instantáneo |

---

## Estructura de Archivos

```
FinanceApp/
│
├── backend/                      # Backend (API)
│   ├── main.py                   # Endpoints de la API
│   ├── models.py                 # Modelos de BD (tablas)
│   ├── schemas.py                # Esquemas de validación
│   ├── services.py               # Lógica de negocio
│   ├── database.py               # Configuración de BD
│   ├── auth.py                   # Autenticación JWT
│   ├── requirements.txt          # Dependencias Python
│   ├── finance.db                # Base de datos SQLite
│   └── .env                      # Variables de entorno
│
├── frontend/                     # Frontend (Vue)
│   ├── src/
│   │   ├── main.js               # Punto de entrada
│   │   ├── App.vue               # Componente raíz
│   │   ├── style.css             # Estilos globales
│   │   ├── router/
│   │   │   └── index.js          # Configuración de rutas
│   │   ├── stores/               # Estado global (Pinia)
│   │   │   ├── auth.js           # Autenticación
│   │   │   ├── finance.js        # Datos financieros
│   │   │   ├── ai.js             # AI Assistant
│   │   │   └── theme.js          # Dark mode
│   │   └── views/                # Páginas
│   │       ├── Login.vue
│   │       ├── Register.vue
│   │       ├── Dashboard.vue
│   │       ├── Accounts.vue
│   │       ├── Transactions.vue
│   │       ├── Goals.vue
│   │       ├── Analytics.vue
│   │       └── AIAssistant.vue
│   ├── index.html                # HTML base
│   ├── package.json              # Dependencias npm
│   ├── vite.config.js            # Config de Vite
│   └── tailwind.config.js        # Config de Tailwind
│
├── ARQUITECTURA_BACKEND.md       # Documentación backend
├── ARQUITECTURA_FRONTEND.md      # Documentación frontend
├── README_COMPLETO.md             # Este archivo
└── AI_SETUP.md                    # Guía de configuración IA
```

---

## Instalación y Configuración

### **Requisitos Previos:**
- Python 3.9+
- Node.js 16+
- npm o yarn

### **Backend:**

```bash
# 1. Navegar a la carpeta backend
cd backend

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Configurar OpenAI
# Crear archivo .env:
OPENAI_API_KEY=tu-clave-aqui

# 5. Iniciar servidor
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend:**

```bash
# 1. Navegar a la carpeta frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev
```

### **Acceder a la aplicación:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

---

## Seguridad

### **Medidas Implementadas:**

1. **Contraseñas:**
   - Hasheadas con bcrypt (cost factor 12)
   - Nunca se almacenan en texto plano
   - No se envían en respuestas

2. **Tokens JWT:**
   - Firmados con clave secreta
   - Expiran en 30 minutos
   - Se validan en cada petición

3. **Autenticación:**
   - Requerida en todos los endpoints sensibles
   - Usuarios solo acceden a sus propios datos
   - Validación de permisos en backend

4. **Validación de Datos:**
   - Pydantic valida entrada en backend
   - Vue valida en frontend
   - SQL injection prevention (SQLAlchemy ORM)

5. **CORS:**
   - Configurado para permitir solo frontend
   - Previene peticiones de orígenes no autorizados

---

## Métricas y Cálculos

### **Balance Total:**
```python
total_balance = sum(account.current_balance for account in user_accounts)
```

### **Ingresos del Mes:**
```python
monthly_income = sum(
    t.amount for t in transactions 
    if t.transaction_type == 'income' 
    and t.transaction_date.month == current_month
)
```

### **Gastos del Mes:**
```python
monthly_expenses = sum(
    t.amount for t in transactions 
    if t.transaction_type == 'expense' 
    and t.transaction_date.month == current_month
)
```

### **Tasa de Ahorro:**
```python
if monthly_income > 0:
    savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100
else:
    savings_rate = 0
```

### **Progreso de Objetivo:**
```python
progress_percentage = (current_amount / target_amount) * 100
```

### **Financial Health Score (0-100):**
```python
score = 50  # Base

# Savings rate (0-30 pts)
if savings_rate >= 20: score += 30
elif savings_rate >= 10: score += 20
elif savings_rate >= 5: score += 10

# Income vs expenses (0-20 pts)
if net_income > 0: score += 20
elif net_income >= -100: score += 10

# Account diversity (0-20 pts)
score += min(num_different_account_types * 5, 20)

# Goal progress (0-10 pts)
score += min(average_goal_progress * 10, 10)

return min(max(score, 0), 100)  # Clamp entre 0-100
```

---

## Conceptos Clave para Explicar

### **1. SPA (Single Page Application):**
- Una sola página HTML que se actualiza dinámicamente
- No recarga completa al navegar
- Más rápida y mejor experiencia de usuario

### **2. REST API:**
- Interfaz que permite comunicación cliente-servidor
- Usa HTTP methods (GET, POST, PUT, DELETE)
- Intercambia datos en formato JSON

### **3. Reactive Programming (Vue):**
- Los datos y la UI están sincronizados
- Cambiar un dato actualiza automáticamente la vista
- Declarativo en lugar de imperativo

### **4. State Management (Pinia):**
- Almacén centralizado de datos
- Accesible desde cualquier componente
- Evita prop drilling

### **5. JWT Authentication:**
- Token codificado que contiene user_id
- Se envía en cada petición
- Backend lo verifica y extrae el usuario

### **6. ORM (Object-Relational Mapping):**
- Abstrae SQL con objetos Python
- `user.accounts` en lugar de `SELECT * FROM accounts WHERE user_id=?`
- Previene SQL injection

---

## Soporte y Recursos

### **Documentación de Referencia:**
- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pinia](https://pinia.vuejs.org/)
- [Chart.js](https://www.chartjs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

### **Archivos de Documentación:**
1. `ARQUITECTURA_BACKEND.md` - Explicación detallada del backend
2. `ARQUITECTURA_FRONTEND.md` - Explicación detallada del frontend
3. `AI_SETUP.md` - Configuración del asistente de IA
4. `README_COMPLETO.md` - Este archivo (visión general)

---

**¡Ahora puedes explicar cada parte de tu aplicación con confianza!**
