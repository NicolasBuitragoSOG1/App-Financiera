# Diagrama Completo - FinanceApp

## Arquitectura y Flujo Completo del Sistema

```mermaid
graph TB
    subgraph "USUARIO"
        U[Usuario Final<br/>Navegador Web]
    end

    subgraph "FRONTEND - Vue.js 3"
        V[Vue Router<br/>8 Rutas]
        
        subgraph "Vistas"
            V1[Login/Register]
            V2[Dashboard]
            V3[Cuentas]
            V4[Transacciones]
            V5[Metas]
            V6[Analytics]
            V7[AI Assistant]
        end
        
        subgraph "Pinia Stores"
            S1[authStore<br/>JWT Token]
            S2[financeStore<br/>Datos financieros]
            S3[aiStore<br/>Consultas IA]
        end
    end

    subgraph "BACKEND - FastAPI Python"
        API[API REST FastAPI<br/>Puerto 8000]
        AUTH[AuthService<br/>JWT + bcrypt]
        
        subgraph "Services - Lógica de Negocio"
            SV1[UserService<br/>create_user<br/>get_user_by_email]
            SV2[AccountService<br/>create_account<br/>get_user_accounts<br/>update_balance<br/>delete_account]
            SV3[TransactionService<br/>create_transaction<br/>get_user_transactions<br/>validate_date_and_balance]
            SV4[FinancialGoalService<br/>create_goal<br/>update_goal_progress<br/>get_user_goals]
            SV5[AnalyticsService<br/>calculate_monthly_metrics<br/>get_financial_overview<br/>calculate_savings_rate]
            SV6[AIAssistantService<br/>get_financial_advice<br/>OpenAI Integration<br/>Fallback Rules]
            SV7[BankingPlatformService<br/>manage_platforms]
        end
    end

    subgraph "BASE DE DATOS - SQLite"
        subgraph "Tablas Principales"
            T1[(users<br/>id, email, password<br/>full_name, is_active)]
            T2[(accounts<br/>id, user_id, platform_id<br/>account_name, balance<br/>account_type, currency)]
            T3[(transactions<br/>id, user_id, account_id<br/>type, amount, category<br/>description, date)]
            T4[(financial_goals<br/>id, user_id, goal_name<br/>target_amount, current<br/>priority, target_date)]
            T5[(financial_metrics<br/>id, user_id, metric_name<br/>value, period)]
            T6[(banking_platforms<br/>id, name, type<br/>logo_url)]
        end
    end

    subgraph "APIS EXTERNAS"
        OPENAI[OpenAI GPT-3.5<br/>Financial Advice<br/>Personalized Tips]
    end

    %% Conexiones Usuario -> Frontend
    U -->|Interactúa| V
    V --> V1 & V2 & V3 & V4 & V5 & V6 & V7
    V1 --> S1
    V2 & V3 & V4 & V5 & V6 --> S2
    V7 --> S3

    %% Conexiones Frontend -> Backend
    S1 -->|POST /api/login<br/>POST /api/register| AUTH
    S2 -->|HTTP REST<br/>Bearer Token| API
    S3 -->|POST /api/ai/advice| API

    %% Conexiones Backend API -> Services
    AUTH --> SV1
    API --> SV2 & SV3 & SV4 & SV5 & SV6 & SV7

    %% Conexiones Services -> Database
    SV1 -->|CRUD Users| T1
    SV2 -->|CRUD Accounts| T2
    SV3 -->|CRUD Transactions<br/>Update Balance| T3
    SV3 -->|Auto Update| T2
    SV4 -->|CRUD Goals| T4
    SV5 -->|Calculate & Store| T5
    SV5 -->|Query All| T1 & T2 & T3 & T4
    SV7 -->|CRUD Platforms| T6

    %% Relaciones Database
    T1 -.1:N.-> T2
    T1 -.1:N.-> T3
    T1 -.1:N.-> T4
    T1 -.1:N.-> T5
    T6 -.1:N.-> T2
    T2 -.1:N.-> T3

    %% API Externa
    SV6 -->|API Call<br/>Contexto Financiero| OPENAI
    OPENAI -.->|AI Response| SV6

    %% Estilos
    classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef backend fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef database fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef external fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef user fill:#fce4ec,stroke:#c2185b,stroke-width:3px

    class U user
    class V,V1,V2,V3,V4,V5,V6,V7,S1,S2,S3 frontend
    class API,AUTH,SV1,SV2,SV3,SV4,SV5,SV6,SV7 backend
    class T1,T2,T3,T4,T5,T6 database
    class OPENAI external
```

---

## Componentes del Sistema

### Frontend (Vue.js 3)
- **8 Vistas:** Login, Register, Dashboard, Cuentas, Transacciones, Metas, Analytics, AI Assistant
- **3 Stores (Pinia):** authStore (autenticación), financeStore (datos), aiStore (IA)
- **Tecnologías:** Vue Router, Axios, TailwindCSS, Vite

### Backend (FastAPI Python)
- **7 Servicios principales:**
  1. **UserService** - Gestión de usuarios y registro
  2. **AccountService** - CRUD de cuentas bancarias
  3. **TransactionService** - Ingresos, gastos, transferencias
  4. **FinancialGoalService** - Metas financieras con progreso
  5. **AnalyticsService** - Métricas y dashboard
  6. **AIAssistantService** - Asesoría con OpenAI/Reglas
  7. **BankingPlatformService** - Catálogo de plataformas

### Base de Datos (SQLite)
- **6 Tablas:**
  - `users` - Usuarios del sistema
  - `accounts` - Cuentas bancarias (checking, savings, credit, investment)
  - `transactions` - Movimientos financieros (income, expense, transfer)
  - `financial_goals` - Metas con tracking de progreso
  - `financial_metrics` - Métricas calculadas históricas
  - `banking_platforms` - Bancos y plataformas digitales

### APIs Externas
- **OpenAI GPT-3.5:** Asesoría financiera personalizada
- **Fallback:** Sistema basado en reglas si no hay API key

---

## Flujos Principales

### 1. Autenticación
```
Usuario → Login Form → POST /api/login → AuthService
→ Verify password (bcrypt) → Generate JWT Token
→ Return Token → Store in authStore → Access granted
```

### 2. Crear Transacción
```
Usuario → Transaction Form → POST /api/transactions
→ Validate: date ≤ NOW, amount > 0, user owns account
→ IF EXPENSE: Check balance ≥ amount
→ Create transaction in DB
→ Auto update account.balance (± amount)
→ Return success → Update UI
```

### 3. Dashboard Financiero
```
Usuario → Dashboard → GET /api/analytics/overview
→ AnalyticsService.get_financial_overview()
→ Query: accounts, transactions, goals
→ Calculate: total_balance, monthly_income, monthly_expenses, savings_rate
→ Return FinancialOverview → Display in UI
```

### 4. Consulta Asistente IA
```
Usuario → AI Assistant → POST /api/ai/advice
→ Get user financial context (overview)
→ IF OpenAI Key exists:
    → Call GPT-3.5 with context → AI Response (confidence: 0.95)
→ ELSE:
    → Rule-based system → Generated Response (confidence: 0.85)
→ Generate recommendations (savings, budget, goals)
→ Return AIResponse → Display advice
```

---

## Funcionalidades Clave

### Validaciones Automáticas
- Transacciones: fecha no futura, saldo suficiente
- Cuentas: usuario propietario, plataforma existe
- Metas: target amount > 0, fecha futura
- Autenticación: JWT válido en cada request

### Actualizaciones Automáticas
- Balance de cuenta al crear transacción
- Métricas mensuales al calcular analytics
- Last_updated timestamp en cambios

### Cálculos Financieros
- Savings Rate = ((income - expenses) / income) × 100
- Goal Progress = (current_amount / target_amount) × 100
- Monthly Metrics por período de fechas

---

## Seguridad

- **Autenticación JWT** (HS256, 30 min expiration)
- **Password Hashing** con bcrypt
- **CORS** configurado para desarrollo
- **Validación de Ownership** en cada operación
- **Bearer Token** en todas las rutas protegidas

---

## Tecnologías

| Capa | Tecnología | Descripción |
|------|-----------|-------------|
| Frontend | Vue.js 3 + Vite | SPA reactivo con HMR |
| State | Pinia | State management moderno |
| Styling | TailwindCSS | Utility-first CSS |
| Backend | FastAPI | Python async framework |
| ORM | SQLAlchemy | Database abstraction |
| Validation | Pydantic | Type validation |
| Auth | JWT + bcrypt | Token-based auth |
| Database | SQLite | Embedded database |
| IA | OpenAI API | GPT-3.5-turbo |

---

## Estadísticas del Sistema

- **Endpoints API:** 18+
- **Servicios:** 7
- **Modelos:** 15+ Pydantic + 6 ORM
- **Vistas Frontend:** 8
- **Stores:** 4
- **Tablas DB:** 6
- **Relaciones:** 8 Foreign Keys

