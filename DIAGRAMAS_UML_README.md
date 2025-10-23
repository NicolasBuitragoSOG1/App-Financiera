# Diagramas UML - FinanceApp

Este documento contiene la documentación completa de los diagramas UML para el proyecto FinanceApp, una aplicación de gestión financiera personal con arquitectura Frontend (Vue.js) y Backend (FastAPI/Python).

## 📋 Índice de Diagramas

1. **UML_Diagrama_Clases.puml** - Diagrama de Clases del Backend
2. **UML_Diagrama_Componentes.puml** - Arquitectura de Componentes del Sistema
3. **UML_Diagrama_Secuencia.puml** - Flujos de Operaciones Principales
4. **UML_Diagrama_Casos_Uso.puml** - Casos de Uso del Usuario
5. **UML_Diagrama_ER.puml** - Modelo Entidad-Relación de la Base de Datos
6. **UML_Diagrama_Arquitectura_General.puml** - Vista General de la Arquitectura
7. **UML_Diagrama_Estado_Transacciones.puml** - Diagrama de Estados de Transacciones
8. **UML_Diagrama_Despliegue.puml** - Infraestructura y Despliegue
9. **UML_Diagrama_Actividad_AI.puml** - Flujo de Actividad del Asistente IA

## 🔧 Cómo Visualizar los Diagramas

Los diagramas están escritos en **PlantUML**, un lenguaje de descripción de diagramas UML basado en texto.

### Opción 1: Visual Studio Code (Recomendado)

1. Instala la extensión **PlantUML** de jebbs
2. Abre cualquier archivo `.puml`
3. Presiona `Alt + D` para ver la vista previa
4. O haz clic derecho → "Preview Current Diagram"

### Opción 2: Online

1. Ve a [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)
2. Copia y pega el contenido de cualquier archivo `.puml`
3. El diagrama se renderizará automáticamente

### Opción 3: Exportar a Imagen

En VS Code con la extensión PlantUML:
- Haz clic derecho en el archivo `.puml`
- Selecciona "Export Current Diagram"
- Elige el formato (PNG, SVG, PDF, etc.)

## 📊 Descripción de Cada Diagrama

### 1. Diagrama de Clases (UML_Diagrama_Clases.puml)

**Propósito:** Muestra la estructura completa del backend, incluyendo:

- **Enums**: Tipos de datos enumerados (AccountType, TransactionType, PlatformType, etc.)
- **Modelos de Base de Datos**: Clases SQLAlchemy que representan las tablas
- **Modelos Pydantic**: Schemas de validación para la API
- **Servicios**: Lógica de negocio organizada por dominio
- **Relaciones**: Conexiones entre entidades (1:N, N:1, etc.)

**Elementos Clave:**
- User, Account, Transaction, FinancialGoal, FinancialMetric
- UserService, AccountService, TransactionService, etc.
- AuthService para autenticación JWT
- AIAssistantService con integración OpenAI

**Colores:**
- 🟡 Amarillo: Enums
- 🔵 Azul: Modelos Pydantic (API)
- 🟢 Verde: Servicios (Business Logic)
- 🔴 Rojo: Modelos de Base de Datos

### 2. Diagrama de Componentes (UML_Diagrama_Componentes.puml)

**Propósito:** Arquitectura general del sistema mostrando:

- **Frontend**: Vue.js 3 con Vistas, Stores (Pinia), y Router
- **Backend**: FastAPI con endpoints, servicios, y modelos
- **Base de Datos**: SQLite con 6 tablas principales
- **APIs Externas**: OpenAI GPT-3.5 para el asistente IA

**Flujo de Datos:**
```
Usuario → Vista (Vue) → Store (Pinia) → API REST → Servicio → Base de Datos
```

**Características:**
- CORS configurado para desarrollo local
- Autenticación JWT en todas las rutas protegidas
- Separación clara entre capas (Frontend/Backend/Database)

### 3. Diagrama de Secuencia (UML_Diagrama_Secuencia.puml)

**Propósito:** Flujos detallados de operaciones críticas:

#### Secuencias Incluidas:

1. **Autenticación**
   - Login con email/password
   - Generación de JWT token
   - Verificación de password con bcrypt

2. **Dashboard**
   - Obtención de overview financiero
   - Cálculo de métricas mensuales
   - Agregación de datos de múltiples fuentes

3. **Crear Transacción**
   - Validaciones (fecha, saldo, permisos)
   - Actualización automática de balance
   - Manejo de errores (saldo insuficiente, etc.)

4. **Consultar Asistente IA**
   - Modo OpenAI (con API key)
   - Modo Fallback (basado en reglas)
   - Generación de recomendaciones personalizadas

5. **Actualizar Meta Financiera**
   - Verificación de pertenencia
   - Actualización de progreso
   - Cálculo de porcentaje completado

**Notación:**
- `→` Llamada síncrona
- `-->` Respuesta
- `alt/else` Flujos condicionales

### 4. Diagrama de Casos de Uso (UML_Diagrama_Casos_Uso.puml)

**Propósito:** Funcionalidades desde la perspectiva del usuario.

#### Paquetes de Funcionalidad:

1. **Gestión de Usuario**
   - Registrarse, Iniciar/Cerrar Sesión, Ver Perfil

2. **Gestión de Cuentas**
   - Crear, Ver, Editar, Eliminar cuentas
   - Actualizar balance, Seleccionar plataforma

3. **Gestión de Transacciones**
   - Registrar ingresos, gastos, transferencias
   - Ver historial con validaciones automáticas

4. **Gestión de Metas Financieras**
   - Crear, Ver, Editar, Eliminar metas
   - Actualizar progreso, Calcular porcentaje

5. **Análisis y Métricas**
   - Dashboard financiero completo
   - Métricas mensuales, Tasa de ahorro
   - Tendencias y resúmenes por plataforma

6. **Asistente Financiero IA**
   - Consultar asesoría personalizada
   - Recomendaciones basadas en datos reales
   - Doble modo: IA (GPT-3.5) o Reglas

**Relaciones:**
- `<<include>>`: Funcionalidad obligatoria
- `<<extend>>`: Funcionalidad opcional
- `<<uses>>`: Comunicación con sistemas externos

### 5. Diagrama Entidad-Relación (UML_Diagrama_ER.puml)

**Propósito:** Modelo de base de datos detallado con:

#### Tablas Principales:

1. **users** (Usuarios del sistema)
   - Email único
   - Password hasheado con bcrypt
   - Soft delete con is_active

2. **banking_platforms** (Catálogo de plataformas)
   - Bancos, billeteras digitales, inversiones, crypto
   - Logo URL y API endpoint opcionales

3. **accounts** (Cuentas del usuario)
   - Múltiples cuentas por usuario
   - Balance en tiempo real
   - Soporte multi-moneda

4. **transactions** (Movimientos financieros)
   - Ingresos, gastos, transferencias
   - Actualización automática de balances
   - Validación de fechas y saldos

5. **financial_goals** (Metas financieras)
   - Target vs Current tracking
   - Priorización (high/medium/low)
   - Cálculo de progreso

6. **financial_metrics** (Métricas calculadas)
   - Ingresos/gastos mensuales
   - Tasa de ahorro
   - Almacenamiento histórico

#### Relaciones:
- **1:N** (Uno a Muchos)
  - Usuario → Cuentas, Transacciones, Metas, Métricas
  - Plataforma → Cuentas
  - Cuenta → Transacciones

#### Constraints:
- Primary Keys en todas las tablas
- Foreign Keys con integridad referencial
- Índices en campos de búsqueda frecuente
- Valores por defecto (is_active, currency, balance)

### 6. Diagrama de Arquitectura General (UML_Diagrama_Arquitectura_General.puml)

**Propósito:** Vista panorámica de toda la arquitectura del sistema.

**Capas del Sistema:**

1. **Capa de Presentación** (Frontend)
   - Vue.js 3 SPA
   - Vue Router para navegación
   - Pinia Stores para state management

2. **Capa de API REST** (Backend)
   - FastAPI con endpoints RESTful
   - JWT Authentication
   - CORS habilitado

3. **Capa de Negocio** (Services)
   - Service Layer Pattern
   - Business Logic y validaciones
   - Cálculos financieros

4. **Capa de Datos** (Database)
   - SQLAlchemy ORM
   - SQLite Database
   - Pydantic Models para validación

**Flujo Completo:**
```
Usuario → Vista → Store → API REST → Service → ORM → Database
                                   ↓
                              OpenAI API (opcional)
```

**Patrones Implementados:**
- Service Layer, Repository Pattern, DTO Pattern
- Dependency Injection, JWT Authentication
- MVVM, Component-based, Store Pattern

### 7. Diagrama de Estados - Transacciones (UML_Diagrama_Estado_Transacciones.puml)

**Propósito:** Modelar los estados por los que pasa una transacción.

**Estados Principales:**
1. **Seleccionando Cuenta** - Usuario elige cuenta origen
2. **Ingresando Datos** - Formulario de transacción
3. **Validando Datos** - Verificación de reglas de negocio
4. **Verificando Saldo** - Solo para EXPENSE
5. **Procesando Transacción** - Creación en DB
6. **Actualizando Balance** - Modificación automática del balance
7. **Transacción Exitosa** - Completada
8. **Error en Transacción** - Fallo en algún paso

**Transiciones:**
- Validación exitosa → Procesamiento
- Validación fallida → Error
- Saldo insuficiente → Error
- Error → Usuario puede corregir

**Validaciones del Sistema:**
- Fecha no en el futuro
- Monto > 0
- Cuenta pertenece al usuario
- Saldo suficiente (EXPENSE)

### 8. Diagrama de Despliegue (UML_Diagrama_Despliegue.puml)

**Propósito:** Infraestructura física y lógica del sistema.

**Entornos:**

#### Desarrollo Local
- **Cliente**: Navegador Web
- **Frontend**: Vite Dev Server (localhost:3000)
- **Backend**: Uvicorn ASGI Server (localhost:8000)
- **Database**: SQLite archivo local
- **Características**: HMR, Auto-reload, CORS habilitado

#### Producción (Docker)
- **Frontend Container**: Nginx + Vue App (built)
- **Backend Container**: FastAPI + Uvicorn
- **Database**: Persistent Volume (SQLite/PostgreSQL)
- **Network**: Docker internal network

**Opciones de Despliegue:**
1. **Desarrollo Local** - Sin contenedores
2. **Docker Compose** - Containerizado local
3. **Cloud** - Netlify (Frontend) + Heroku (Backend)
4. **VPS** - Nginx + Gunicorn + PostgreSQL

**Seguridad:**
- HTTPS con certificados SSL
- CORS configurado por dominio
- Variables de entorno para secrets
- Rate limiting con Nginx

### 9. Diagrama de Actividad - Asistente IA (UML_Diagrama_Actividad_AI.puml)

**Propósito:** Flujo detallado del proceso de asesoría financiera con IA.

**Flujo Principal:**
1. Usuario ingresa pregunta financiera
2. Frontend valida y envía a API
3. AIAssistantService obtiene contexto financiero completo
4. AnalyticsService consulta todas las métricas del usuario
5. Sistema decide entre dos modos:

   **Modo A: OpenAI API (si API key disponible)**
   - Prepara prompt con contexto
   - Llama a GPT-3.5-turbo
   - Recibe respuesta personalizada
   - Confidence: 0.95

   **Modo B: Sistema de Reglas (Fallback)**
   - Analiza keywords en query
   - Aplica reglas basadas en métricas
   - Genera respuesta estructurada
   - Confidence: 0.85

6. Genera recomendaciones automáticas
7. Retorna AIResponse completo
8. Frontend muestra asesoría al usuario

**Tipos de Consultas Soportadas:**
- Ahorro (savings)
- Presupuesto (budget)
- Metas (goals)
- Inversión (invest)
- Deuda (debt)
- General (overview)

**Recomendaciones Automáticas:**
- Basadas en savings_rate
- Basadas en expense ratio
- Basadas en active goals
- Basadas en diversificación de cuentas

## 🎨 Convenciones de Color

- **🟡 Amarillo**: Enumeraciones (Enums)
- **🔵 Azul**: Modelos/Componentes Frontend
- **🟢 Verde**: Servicios/Lógica de Negocio
- **🔴 Rojo**: Base de Datos/Persistencia
- **🟠 Naranja**: Casos de Uso/Actores

## 📝 Notas Importantes

### Seguridad
- Autenticación JWT con tokens de 30 minutos
- Passwords hasheados con bcrypt
- Validación de permisos en cada operación
- CORS configurado para desarrollo

### Validaciones Clave
1. **Transacciones**
   - Fecha no puede ser futura
   - Saldo suficiente para gastos
   - Cuenta pertenece al usuario
   - Monto mayor a 0

2. **Cuentas**
   - Plataforma debe existir
   - Usuario es dueño de la cuenta
   - Soft delete (no eliminación real)

3. **Metas**
   - Target amount > 0
   - Fecha objetivo en el futuro
   - Progreso calculado automáticamente

### Asistente IA
- **Modo 1**: OpenAI GPT-3.5 (requiere API key)
  - Respuestas personalizadas y contextuales
  - Confidence: 0.95
- **Modo 2**: Sistema basado en reglas (fallback)
  - Sin dependencias externas
  - Confidence: 0.85

## 🚀 Tecnologías Documentadas

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Autenticación**: JWT + bcrypt
- **Base de Datos**: SQLite
- **IA**: OpenAI API (opcional)

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **Styling**: TailwindCSS
- **HTTP Client**: Axios

## 📚 Recursos Adicionales

- [PlantUML Documentation](https://plantuml.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js 3 Guide](https://vuejs.org/guide/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

## 🔄 Actualización de Diagramas

Si realizas cambios en el código, actualiza los diagramas correspondientes:

1. Cambios en modelos → `UML_Diagrama_Clases.puml` y `UML_Diagrama_ER.puml`
2. Nuevos endpoints → `UML_Diagrama_Componentes.puml` y `UML_Diagrama_Secuencia.puml`
3. Nuevas funcionalidades → `UML_Diagrama_Casos_Uso.puml`

## 📧 Contacto

Para preguntas sobre los diagramas o la arquitectura del sistema, consulta:
- README.md principal del proyecto
- ARQUITECTURA_BACKEND.md
- ARQUITECTURA_FRONTEND.md

---

**Versión**: 1.0
**Última actualización**: 2024
**Autor**: Sistema de Documentación FinanceApp
