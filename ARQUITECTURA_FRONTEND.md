# 📚 Arquitectura del Frontend - Guía Resumida

## 🏗️ Estructura General

El frontend está construido con **Vue.js 3** (framework JavaScript) y sigue el patrón de **componentes reutilizables** y **gestión de estado centralizada**.

```
frontend/
├── src/
│   ├── main.js              # Punto de entrada de la aplicación
│   ├── App.vue              # Componente principal (layout general)
│   ├── router/
│   │   └── index.js         # Configuración de rutas (navegación)
│   ├── stores/              # Estado global de la aplicación (Pinia)
│   │   ├── auth.js          # Estado de autenticación
│   │   ├── finance.js       # Datos financieros (cuentas, transacciones, etc.)
│   │   ├── ai.js            # Estado del AI Assistant
│   │   └── theme.js         # Estado del tema (dark/light mode)
│   ├── views/               # Vistas principales (páginas)
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Dashboard.vue
│   │   ├── Accounts.vue
│   │   ├── Transactions.vue
│   │   ├── Goals.vue
│   │   ├── Analytics.vue
│   │   └── AIAssistant.vue
│   └── style.css            # Estilos globales
├── index.html               # HTML base
├── tailwind.config.js       # Configuración de Tailwind CSS
└── package.json             # Dependencias de npm
```

---

## 📦 Archivos Principales

### 1️⃣ **`main.js` - Inicialización**

**¿Qué hace?**
- Crea la aplicación Vue
- Configura plugins (Router, Pinia, Toast)
- Monta la aplicación en el DOM

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import Toast from 'vue-toastification'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())   // Gestión de estado
app.use(router)          // Sistema de rutas
app.use(Toast)           // Notificaciones
app.mount('#app')        // Monta en <div id="app">
```

---

### 2️⃣ **`App.vue` - Layout Principal**

**¿Qué hace?**
- Define la estructura general de la app
- Muestra la sidebar (menú lateral)
- Maneja la navegación entre vistas
- Implementa dark mode

**Estructura:**
```vue
<template>
  <!-- Sidebar (menú izquierdo) -->
  <aside>
    - Logo "Finance Manager"
    - Links de navegación (Dashboard, Accounts, etc.)
    - Botón de dark mode
    - Info del usuario
    - Botón de logout
  </aside>
  
  <!-- Contenido principal -->
  <main>
    <router-view />  <!-- Aquí se cargan las vistas -->
  </main>
</template>
```

**Navegación:**
```javascript
const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Accounts', href: '/accounts', icon: CreditCardIcon },
  { name: 'Transactions', href: '/transactions', icon: ArrowsUpDownIcon },
  { name: 'Goals', href: '/goals', icon: FlagIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'AIAssistant', href: '/ai', icon: SparklesIcon }
]
```

---

### 3️⃣ **Stores (Estado Global con Pinia)**

Los stores mantienen datos que necesitan ser accesibles desde cualquier parte de la app.

#### **`stores/auth.js` - Autenticación**

**Datos que guarda:**
```javascript
- token: String        // Token JWT de sesión
- user: Object         // Datos del usuario logueado
```

**Funciones principales:**
```javascript
- login(email, password)     // Inicia sesión
- register(userData)         // Registra nuevo usuario
- logout()                   // Cierra sesión
- checkAuth()                // Verifica si hay sesión activa
```

**Flujo:**
1. Usuario hace login → recibe token
2. Token se guarda en localStorage (persiste)
3. Todas las peticiones al backend incluyen el token
4. Si token expira → logout automático

---

#### **`stores/finance.js` - Datos Financieros**

**Datos que guarda:**
```javascript
- platforms: []        // Lista de plataformas disponibles
- accounts: []         // Cuentas del usuario
- transactions: []     // Transacciones del usuario
- goals: []           // Objetivos financieros
- overview: {}        // Resumen financiero general
```

**Funciones principales:**
```javascript
// Inicialización
- initializeData()     // Carga todos los datos al inicio

// Cuentas
- createAccount(data)
- updateAccount(id, data)
- deleteAccount(id)

// Transacciones
- createTransaction(data)
- updateTransaction(id, data)
- deleteTransaction(id)

// Objetivos
- createGoal(data)
- updateGoal(id, data)
- deleteGoal(id)

// Analytics
- loadOverview()       // Carga resumen general
```

**Computed Properties (valores calculados):**
```javascript
- totalBalance         // Suma de todas las cuentas
- monthlyIncome        // Ingresos del mes actual
- monthlyExpenses      // Gastos del mes actual
- savingsRate          // Tasa de ahorro
```

---

#### **`stores/theme.js` - Dark Mode**

**Datos que guarda:**
```javascript
- isDark: Boolean      // true = dark mode, false = light mode
```

**Funciones principales:**
```javascript
- initTheme()         // Inicializa tema desde localStorage
- toggleTheme()       // Cambia entre dark/light
- applyTheme()        // Aplica clase 'dark' al HTML
```

**Cómo funciona:**
```javascript
// Al cambiar tema:
1. Cambia isDark
2. Guarda preferencia en localStorage
3. Agrega/quita clase 'dark' del <html>
4. Tailwind CSS aplica estilos dark: automáticamente
```

---

#### **`stores/ai.js` - AI Assistant**

**Datos que guarda:**
```javascript
- chatHistory: []      // Historial de conversación
- isLoading: Boolean   // Estado de carga
```

**Funciones principales:**
```javascript
- getFinancialAdvice(query)    // Envía pregunta a la IA
- clearChatHistory()           // Limpia el chat
```

**Flujo del chat:**
1. Usuario escribe pregunta
2. Se agrega mensaje de usuario al historial
3. Envía petición al backend
4. Backend procesa y responde
5. Se agrega respuesta de IA al historial

---

### 4️⃣ **Vistas (Páginas Principales)**

#### **`Login.vue` y `Register.vue`**

**¿Qué hacen?**
- Formularios de autenticación
- Validación de campos
- Manejo de errores
- Redirección al dashboard después de login

**Componentes:**
- Inputs de email y contraseña
- Botón de submit
- Toggle de dark mode
- Links entre login/register

---

#### **`Dashboard.vue` - Vista Principal**

**¿Qué muestra?**

1. **Tarjetas de resumen:**
   - Balance total
   - Ingresos del mes
   - Gastos del mes
   - Tasa de ahorro

2. **Cuentas por plataforma:**
   - Lista de plataformas con balance
   - Número de cuentas por plataforma

3. **Transacciones recientes:**
   - Últimas 5 transacciones
   - Link para ver todas

4. **Progreso de objetivos:**
   - Lista de objetivos activos
   - Barras de progreso
   - Link para ver todos

**Datos que usa:**
```javascript
const financeStore = useFinanceStore()
- financeStore.totalBalance
- financeStore.overview
- financeStore.accounts
- financeStore.transactions
- financeStore.goals
```

---

#### **`Accounts.vue` - Gestión de Cuentas**

**¿Qué permite hacer?**

1. **Ver cuentas:**
   - Grid de tarjetas
   - Info: nombre, plataforma, tipo, balance

2. **Crear cuenta:**
   - Modal con formulario
   - Selección de plataforma
   - Tipo de cuenta
   - Balance inicial

3. **Editar cuenta:**
   - Modal pre-llenado
   - Actualizar cualquier campo

4. **Eliminar cuenta:**
   - Confirmación antes de eliminar

**Componentes del modal:**
```vue
<select>             <!-- Seleccionar plataforma -->
<select>             <!-- Tipo de cuenta -->
<input type="text">  <!-- Nombre de cuenta -->
<input type="number"> <!-- Balance -->
```

---

#### **`Transactions.vue` - Gestión de Transacciones**

**¿Qué muestra?**

1. **Tabla de transacciones:**
   - Fecha, descripción, categoría, cuenta, monto
   - Orden cronológico (más reciente primero)
   - Color diferente para income/expense

2. **Filtros:**
   - Por tipo (income/expense/all)
   - Por categoría
   - Por cuenta

3. **Acciones:**
   - Crear transacción
   - Editar transacción
   - Eliminar transacción

**Filtrado de datos:**
```javascript
const filteredTransactions = computed(() => {
  return transactions.filter(t => {
    if (filters.type && t.transaction_type !== filters.type) return false
    if (filters.category && t.category !== filters.category) return false
    if (filters.account && t.account_id !== filters.account) return false
    return true
  })
})
```

**Categorías disponibles:**
- Food & Dining
- Transportation
- Shopping
- Bills & Utilities
- Entertainment
- Healthcare
- Education
- Travel
- Personal Care
- Other Expenses

---

#### **`Goals.vue` - Objetivos Financieros**

**¿Qué muestra?**

1. **Tarjetas de objetivos:**
   - Nombre del objetivo
   - Tipo y prioridad
   - Barra de progreso
   - Monto actual vs meta
   - Fecha límite
   - Monto restante

2. **Acciones:**
   - Crear objetivo
   - Actualizar progreso
   - Editar objetivo
   - Eliminar objetivo

**Tipos de objetivos:**
- Savings (Ahorros)
- Debt Reduction (Reducción de deuda)
- Investment (Inversión)

**Prioridades:**
- High (Alta)
- Medium (Media)
- Low (Baja)

**Cálculo de progreso:**
```javascript
const progress = (current_amount / target_amount) * 100
```

---

#### **`Analytics.vue` - Análisis Financiero**

**¿Qué muestra?**

1. **Selector de período:**
   - Año
   - Mes

2. **Métricas principales:**
   - Ingresos del mes
   - Gastos del mes
   - Tasa de ahorro
   - Cambio vs mes anterior

3. **Gráficos (Chart.js):**
   - **Barras**: Income vs Expenses vs Net
   - **Dona**: Distribución de gastos por categoría

4. **Tendencias mensuales:**
   - Ingreso neto
   - Promedio de gasto diario
   - Gasto más grande

5. **Financial Health Score:**
   - Puntuación de 0-100
   - Recomendaciones personalizadas

6. **Tabla de rendimiento de cuentas:**
   - Balance actual
   - Cambio mensual
   - Estado (Growing/Stable)

**Configuración de gráficos:**
```javascript
// Detecta modo oscuro
const isDark = document.documentElement.classList.contains('dark')
const textColor = isDark ? '#e5e7eb' : '#374151'
const gridColor = isDark ? '#4b5563' : '#e5e7eb'

// Aplica colores a Chart.js
options: {
  scales: {
    x: { ticks: { color: textColor } },
    y: { ticks: { color: textColor } }
  }
}
```

---

#### **`AIAssistant.vue` - Asistente de IA**

**¿Qué muestra?**

1. **Área de chat:**
   - Mensajes del usuario (azul, derecha)
   - Mensajes de IA (gris, izquierda)
   - Recomendaciones con iconos
   - Barra de confianza
   - Timestamp de cada mensaje

2. **Panel lateral derecho:**
   - **Financial Snapshot**: Resumen de finanzas
   - **Quick Actions**: Preguntas sugeridas
   - **AI Tips**: Consejos de uso
   - **Clear Chat**: Limpiar historial

3. **Input de chat:**
   - Campo de texto
   - Botón de enviar
   - Indicador de carga

**Flujo de conversación:**
```javascript
1. Usuario escribe y envía
2. Mensaje aparece inmediatamente
3. Indicador "AI is thinking..."
4. Respuesta de IA aparece
5. Auto-scroll al final
```

**Sugerencias rápidas:**
- "How can I improve my savings rate?"
- "What should I budget for next month?"
- "How am I doing with my financial goals?"
- "Should I invest more money?"

---

### 5️⃣ **Router (Navegación)**

**`router/index.js`**

**¿Qué hace?**
- Define las rutas de la aplicación
- Protege rutas que requieren autenticación
- Redirige usuarios no autenticados al login

**Rutas definidas:**
```javascript
- / → Redirect a /login
- /login → Login.vue
- /register → Register.vue
- /dashboard → Dashboard.vue (requiere auth)
- /accounts → Accounts.vue (requiere auth)
- /transactions → Transactions.vue (requiere auth)
- /goals → Goals.vue (requiere auth)
- /analytics → Analytics.vue (requiere auth)
- /ai → AIAssistant.vue (requiere auth)
```

**Protección de rutas:**
```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')  // No autenticado → login
  } else {
    next()          // Autenticado → continuar
  }
})
```

---

### 6️⃣ **Estilos (Tailwind CSS)**

**`tailwind.config.js`**

**Configuración:**
```javascript
darkMode: 'class'    // Dark mode basado en clase CSS
```

**Clases personalizadas (`style.css`):**
```css
.btn-primary         /* Botón azul principal */
.btn-secondary       /* Botón gris secundario */
.card                /* Tarjeta blanca con sombra */
.input-field         /* Campo de input estilizado */
```

**Dark mode:**
```html
<!-- Light mode -->
<div class="bg-white text-gray-900">

<!-- Dark mode (con clase dark: prefix) -->
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
```

**Cómo funciona:**
1. JavaScript agrega clase `dark` al `<html>`
2. Tailwind aplica estilos `dark:` automáticamente
3. Todo cambia de color instantáneamente

---

## 🔄 Flujo de Datos Completo

### Ejemplo: Crear una transacción

1. **Usuario** llena el formulario en `Transactions.vue`

2. **Vista** llama al store:
```javascript
await financeStore.createTransaction({
  account_id: 1,
  transaction_type: 'expense',
  amount: 50.00,
  category: 'Food & Dining',
  description: 'Lunch'
})
```

3. **Store** hace petición HTTP al backend:
```javascript
await axios.post('/api/transactions', data)
```

4. **Backend** crea la transacción y responde

5. **Store** actualiza su lista de transacciones:
```javascript
this.transactions.push(newTransaction)
```

6. **Vista** se actualiza automáticamente (reactive)
   - La tabla muestra la nueva transacción
   - El balance se actualiza

---

## 📊 Tecnologías Clave

- **Vue.js 3**: Framework JavaScript reactivo
- **Pinia**: Gestión de estado (reemplazo de Vuex)
- **Vue Router**: Sistema de navegación
- **Axios**: Cliente HTTP para API
- **Tailwind CSS**: Framework de estilos utility-first
- **Chart.js**: Librería de gráficos
- **Heroicons**: Iconos SVG
- **Vue Toastification**: Notificaciones toast
- **date-fns**: Manipulación de fechas
- **Vite**: Build tool ultra-rápido

---

## 🎨 Sistema de Diseño

### Colores principales:
```javascript
primary: blue (#3b82f6)    // Botones, links
success: green (#10b981)   // Ingresos, éxito
warning: yellow (#f59e0b)  // Advertencias
danger: red (#ef4444)      // Gastos, errores
```

### Tema oscuro:
```javascript
Fondo: gray-900 (#111827)
Cards: gray-800 (#1f2937)
Bordes: gray-700 (#374151)
Texto: white (#ffffff)
Texto secundario: gray-400 (#9ca3af)
```

---

## 🔐 Seguridad en el Frontend

1. **Token en localStorage**
   - Persiste entre sesiones
   - Se envía en header de cada petición

2. **Axios interceptor**
   - Agrega token automáticamente
   - Maneja errores 401 (logout automático)

3. **Validación de formularios**
   - Campos requeridos
   - Tipos de datos correctos
   - Mensajes de error claros

4. **Protección de rutas**
   - Redirige a login si no autenticado
   - Verifica token antes de cargar datos

---

## 💡 Conceptos Clave de Vue.js

### **Reactive Data:**
```javascript
const count = ref(0)      // Se actualiza en la UI automáticamente
count.value = 5           // UI cambia instantáneamente
```

### **Computed Properties:**
```javascript
const total = computed(() => {
  return transactions.reduce((sum, t) => sum + t.amount, 0)
})
// Se recalcula automáticamente cuando transactions cambia
```

### **Watchers:**
```javascript
watch(isDark, () => {
  applyTheme()  // Ejecuta cuando isDark cambia
})
```

### **Lifecycle Hooks:**
```javascript
onMounted(() => {
  loadData()    // Se ejecuta cuando el componente carga
})
```

---

## 📱 Responsive Design

La app es responsive gracias a Tailwind:

```html
<!-- Mobile: 1 columna, Desktop: 3 columnas -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
```

**Breakpoints:**
- `sm`: ≥640px
- `md`: ≥768px
- `lg`: ≥1024px
- `xl`: ≥1280px
