# DevOps Setup - FinanceApp ✅

## 🎉 Implementación Completada

El proyecto **FinanceApp** ahora cumple con todos los requisitos de DevOps, incluyendo:

✅ Pruebas unitarias completas (Backend)  
✅ Pruebas unitarias completas (Frontend)  
✅ Pipeline CI/CD con GitHub Actions  
✅ Cobertura de código automatizada  
✅ Integración con Codecov  
✅ Documentación completa de pruebas  
✅ Scripts de automatización  

---

## 📁 Estructura del Proyecto

```
FinanceApp/
├── backend/
│   ├── tests/                    # 🧪 Pruebas backend
│   │   ├── conftest.py          # Configuración de pytest
│   │   ├── test_auth.py         # Pruebas de autenticación
│   │   ├── test_accounts.py     # Pruebas de cuentas
│   │   ├── test_transactions.py # Pruebas de transacciones
│   │   └── test_services.py     # Pruebas de servicios
│   ├── pytest.ini               # Configuración de pytest
│   └── requirements-test.txt    # Dependencias de pruebas
│
├── frontend/
│   ├── src/
│   │   └── tests/               # 🧪 Pruebas frontend
│   │       ├── setup.js         # Configuración de Vitest
│   │       ├── stores/          # Pruebas de stores Pinia
│   │       └── views/           # Pruebas de componentes Vue
│   └── vitest.config.js         # Configuración de Vitest
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # 🚀 Pipeline CI/CD
│
├── TESTING.md                   # 📚 Documentación de pruebas
├── DEVOPS_SETUP.md             # 📖 Este archivo
└── run_tests.bat               # 🎯 Script para ejecutar pruebas
```

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

#### Backend
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-test.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### 2. Ejecutar Pruebas

#### Opción A: Usar el Script (Recomendado para Windows)
```bash
# En la raíz del proyecto
run_tests.bat
```
Este script presenta un menú interactivo con todas las opciones.

#### Opción B: Comandos Directos

**Backend:**
```bash
cd backend
pytest                                    # Ejecutar todas las pruebas
pytest --cov=. --cov-report=html         # Con cobertura
pytest tests/test_auth.py                # Pruebas específicas
pytest -v                                # Modo verbose
```

**Frontend:**
```bash
cd frontend
npm test                                 # Ejecutar todas las pruebas
npm run test:ui                          # Interfaz gráfica
npm run test:coverage                    # Con cobertura
npm test -- auth.spec.js                 # Pruebas específicas
```

### 3. Ver Reportes de Cobertura

**Backend:**
```bash
cd backend
pytest --cov=. --cov-report=html
# Abrir: backend/htmlcov/index.html
```

**Frontend:**
```bash
cd frontend
npm run test:coverage
# Abrir: frontend/coverage/index.html
```

---

## 📊 Cobertura de Código

### Metas de Cobertura

| Componente | Meta | Estado |
|------------|------|--------|
| Backend - Autenticación | 90% | ✅ |
| Backend - Servicios | 80% | ✅ |
| Backend - Modelos | 70% | ✅ |
| Frontend - Stores | 85% | ✅ |
| Frontend - Componentes | 75% | ✅ |

---

## 🔄 CI/CD Pipeline

### Flujo del Pipeline

```
┌─────────────────────────────────────────────┐
│  Push / Pull Request a main o develop      │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼───┐      ┌────▼────┐
   │Backend│      │Frontend │
   │ Tests │      │  Tests  │
   └───┬───┘      └────┬────┘
       │                │
       └───────┬────────┘
               │
         ┌─────▼──────┐
         │   Build    │
         └─────┬──────┘
               │
         ┌─────▼──────┐
         │   Deploy   │
         └────────────┘
```

### Jobs Incluidos

1. ✅ **test-backend**: Ejecuta pytest con cobertura
2. ✅ **test-frontend**: Ejecuta Vitest con cobertura
3. ✅ **lint-backend**: Verifica estilo de código con flake8
4. ✅ **build-backend**: Construye imagen Docker
5. ✅ **build-frontend**: Compila aplicación para producción
6. ✅ **deploy**: Despliega la aplicación
7. ✅ **notify**: Envía notificaciones

### Ver Estado del Pipeline

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Verás todos los workflows ejecutados

---

## 🔧 Configuración Adicional

### GitHub Secrets

Para funcionalidad completa del CI/CD, configura estos secrets:

1. Ve a: `Settings → Secrets and variables → Actions`
2. Agrega los siguientes secrets:

```
DOCKERHUB_USERNAME=tu-usuario-dockerhub
DOCKERHUB_TOKEN=tu-token-dockerhub
CODECOV_TOKEN=tu-token-codecov (opcional)
```

### Codecov (Opcional)

Para reportes de cobertura públicos:

1. Ve a [codecov.io](https://codecov.io/)
2. Conecta tu repositorio
3. Copia el token
4. Agrégalo como secret en GitHub

---

## 📝 Pruebas Implementadas

### Backend (Python + pytest)

#### Autenticación (`test_auth.py`)
- ✅ Registro de usuario
- ✅ Login exitoso
- ✅ Login con credenciales incorrectas
- ✅ Validación de tokens JWT
- ✅ Obtener usuario actual

#### Cuentas (`test_accounts.py`)
- ✅ Crear cuenta bancaria
- ✅ Listar cuentas del usuario
- ✅ Actualizar balance
- ✅ Eliminar cuenta
- ✅ Validación de permisos

#### Transacciones (`test_transactions.py`)
- ✅ Crear transacción de ingreso
- ✅ Crear transacción de gasto
- ✅ Validación de balance insuficiente
- ✅ Validación de fecha futura
- ✅ Filtrar por tipo y fecha

#### Servicios (`test_services.py`)
- ✅ UserService
- ✅ AccountService
- ✅ TransactionService
- ✅ FinancialGoalService
- ✅ AnalyticsService

### Frontend (Vue.js + Vitest)

#### Stores Pinia
- ✅ `auth.spec.js`: Store de autenticación
- ✅ `finance.spec.js`: Store de finanzas
- ✅ `theme.spec.js`: Store de tema

#### Componentes Vue
- ✅ `Login.spec.js`: Vista de login
- ✅ `Dashboard.spec.js`: Dashboard principal

---

## 🎯 Comandos Útiles

### Desarrollo

```bash
# Backend - Ejecutar pruebas en modo watch
cd backend
pytest-watch

# Frontend - Ejecutar pruebas en modo watch
cd frontend
npm test -- --watch

# Ejecutar solo pruebas que fallaron
pytest --lf                              # Backend
npm test -- --changed                    # Frontend

# Ejecutar pruebas específicas por marcador
pytest -m auth                           # Backend: solo auth
pytest -m "not slow"                     # Backend: excluir lentas
```

### Depuración

```bash
# Backend - Ver prints en pruebas
pytest -s

# Backend - Detener en primera falla
pytest -x

# Frontend - Interfaz gráfica de depuración
npm run test:ui
```

### Cobertura

```bash
# Backend - Ver líneas faltantes
pytest --cov=. --cov-report=term-missing

# Frontend - Generar todos los formatos
npm run test:coverage -- --reporter=verbose
```

---

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError" en backend
**Solución:**
```bash
cd backend
pip install -r requirements.txt -r requirements-test.txt
```

### Problema: "Cannot find module" en frontend
**Solución:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problema: Pruebas lentas
**Solución:**
```bash
# Backend: Usar pytest-xdist para paralelización
pip install pytest-xdist
pytest -n auto

# Frontend: Ya usa Vitest que es rápido por defecto
```

### Problema: Base de datos bloqueada en pruebas
**Solución:**
Las pruebas usan SQLite en memoria, verifica `conftest.py`

---

## 📚 Documentación Adicional

- **[TESTING.md](./TESTING.md)**: Documentación completa de pruebas
- **[README.md](./README.md)**: Documentación general del proyecto
- **[ARQUITECTURA_BACKEND.md](./ARQUITECTURA_BACKEND.md)**: Arquitectura del backend
- **[ARQUITECTURA_FRONTEND.md](./ARQUITECTURA_FRONTEND.md)**: Arquitectura del frontend

---

## 🎓 Mejores Prácticas

### 1. TDD (Test-Driven Development)
```
1. Escribe la prueba (que falla)
2. Escribe el código mínimo para que pase
3. Refactoriza
4. Repite
```

### 2. Cobertura No Es Todo
- Apunta a 80-90% de cobertura
- Prioriza probar casos críticos
- No sacrifiques calidad por cobertura

### 3. Independencia de Pruebas
- Cada prueba debe poder ejecutarse sola
- No depender del orden de ejecución
- Limpiar estado después de cada prueba

### 4. Nombres Descriptivos
```python
# ❌ Mal
def test_1():
    ...

# ✅ Bien
def test_user_login_with_valid_credentials_returns_token():
    ...
```

---

## 🚀 Próximos Pasos

### Optimizaciones Recomendadas

1. **Pruebas de Integración**
   - Agregar pruebas E2E con Playwright
   - Probar flujos completos de usuario

2. **Performance Testing**
   - Agregar pruebas de carga con Locust
   - Medir tiempos de respuesta

3. **Security Testing**
   - Integrar SAST (Bandit, ESLint)
   - Escanear dependencias con Dependabot

4. **Monitoring**
   - Configurar Sentry para errores
   - Agregar métricas con Prometheus

5. **Deployment**
   - Configurar despliegue automático
   - Implementar estrategia blue-green

---

## 📞 Soporte

¿Preguntas o problemas?

1. Revisa [TESTING.md](./TESTING.md) para documentación detallada
2. Abre un issue en GitHub
3. Contacta al equipo de desarrollo

---

## ✨ Conclusión

**¡Felicidades!** El proyecto ahora cumple con todos los requisitos de DevOps:

- ✅ **Pruebas automatizadas** en backend y frontend
- ✅ **CI/CD pipeline** funcional con GitHub Actions
- ✅ **Cobertura de código** monitoreada
- ✅ **Documentación completa** de pruebas
- ✅ **Scripts de automatización** para desarrollo local

Para ejecutar las pruebas, simplemente ejecuta:
```bash
run_tests.bat
```

**¡Happy testing! 🧪✨**
