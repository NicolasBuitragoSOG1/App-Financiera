# Plataforma de Gestión Financiera Personal

## Descripción
Sistema web para registro y gestión de finanzas personales con visualización unificada de saldos, análisis automatizado y asistente de IA.

## Arquitectura
- **Patrón**: MVVM (Model-View-ViewModel)
- **Metodología**: Incremental + DevOps
- **Frontend**: Vue.js 3 con Composition API
- **Backend**: FastAPI con Python
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **IA**: OpenAI GPT para asistente financiero

## Objetivos Específicos
1. Visualización de saldos entre plataformas bancarias (separado y unificado)
2. Métricas y análisis automatizados de gestión financiera
3. Metas y proyecciones financieras por producto
4. Asistente de IA para cumplimiento de proyecciones

## Estructura del Proyecto
```
├── backend/           # FastAPI backend
├── frontend/          # Vue.js frontend
├── docker-compose.yml # DevOps configuration
└── README.md
```

## Instalación y Ejecución

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
```bash
# Ejecutar el script de configuración
setup.bat

# Iniciar la aplicación
start.bat
```

### Opción 2: Instalación Manual
```bash
# Backend
cd backend
pip install -r requirements.txt
python init_data.py
uvicorn main:app --reload

# Frontend (en otra terminal)
cd frontend
npm install
npm run dev
```

## Configuración

### Variables de Entorno
Edita `backend/.env` y configura:
```
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite:///./finance_app.db
```

### Acceso a la Aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Credenciales de Prueba
- Email: user@test.com
- Contraseña: Test123

## Características Principales

### 1. Dashboard Financiero
- Visualización unificada de saldos de todas las plataformas
- Métricas clave: ingresos, gastos, tasa de ahorro
- Resumen de cuentas por plataforma bancaria
- Transacciones recientes y metas financieras

### 2. Gestión de Cuentas
- Soporte para múltiples plataformas bancarias
- Tipos de cuenta: checking, savings, credit, investment
- Actualización manual de saldos
- Categorización por tipo de plataforma

### 3. Seguimiento de Transacciones
- Registro de ingresos, gastos y transferencias
- Categorización automática
- Filtros avanzados por tipo, categoría y cuenta
- Historial completo de movimientos

### 4. Metas Financieras
- Creación de objetivos de ahorro e inversión
- Seguimiento de progreso visual
- Priorización de metas (alta, media, baja)
- Fechas objetivo y montos específicos

### 5. Análisis y Métricas
- Cálculo automático de métricas financieras
- Gráficos de ingresos vs gastos
- Análisis de categorías de gastos
- Score de salud financiera
- Tendencias mensuales y recomendaciones

### 6. Asistente de IA
- Consejos financieros personalizados
- Análisis de patrones de gasto
- Recomendaciones de ahorro e inversión
- Chat interactivo con contexto financiero

## Arquitectura Técnica

### Patrón MVVM Implementado
- **Model**: SQLAlchemy models (database.py)
- **View**: Vue.js components (frontend/src/views/)
- **ViewModel**: Pinia stores (frontend/src/stores/)

### Stack Tecnológico
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL/SQLite
- **Frontend**: Vue.js 3 + Pinia + Tailwind CSS
- **IA**: OpenAI GPT-3.5 para asistente financiero
- **Visualización**: Chart.js para gráficos
- **DevOps**: Docker + Docker Compose

### Metodología Incremental
El desarrollo siguió un enfoque incremental con entregas funcionales:
1. ✅ Autenticación y estructura base
2. ✅ Gestión de cuentas y plataformas
3. ✅ Sistema de transacciones
4. ✅ Metas y objetivos financieros
5. ✅ Analytics y métricas automatizadas
6. ✅ Asistente de IA integrado
7. ✅ DevOps y deployment

## Deployment

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas de despliegue en producción.

### Docker
```bash
# Configurar variable de entorno
export OPENAI_API_KEY=your-api-key

# Iniciar con Docker Compose
docker-compose up -d
```
