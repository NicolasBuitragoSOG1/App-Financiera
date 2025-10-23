# 🤖 AI Assistant Setup Guide

## Configuración de la API de OpenAI

El AI Assistant ahora usa la API de OpenAI (GPT-3.5-turbo) para proporcionar consejos financieros inteligentes y personalizados.

### 📋 Pasos para Configurar:

#### 1️⃣ Obtener API Key de OpenAI

1. **Crear cuenta en OpenAI:**
   - Ve a https://platform.openai.com/signup
   - Regístrate con tu email o cuenta de Google

2. **Obtener API Key:**
   - Ve a https://platform.openai.com/api-keys
   - Haz clic en "Create new secret key"
   - Copia la clave (empieza con `sk-...`)
   - ⚠️ **IMPORTANTE**: Guárdala en un lugar seguro, no la compartás

3. **Agregar créditos (opcional para testing):**
   - OpenAI da $5 USD de crédito gratuito para nuevas cuentas
   - Si necesitas más: https://platform.openai.com/account/billing

#### 2️⃣ Configurar en el Backend

1. **Crear archivo `.env`:**
   ```bash
   cd C:\Users\nicob\OneDrive\Escritorio\FinanceApp\backend
   copy .env.example .env
   ```

2. **Editar `.env`:**
   ```env
   OPENAI_API_KEY=sk-tu-clave-aqui
   DATABASE_URL=sqlite:///./finance.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Reiniciar el backend:**
   - El servidor debe detectar automáticamente el cambio
   - Si no, reinicia manualmente

#### 3️⃣ Verificar Funcionamiento

1. Ve a la vista **AI Assistant** en la app
2. Escribe una pregunta como: "How can I improve my savings?"
3. Deberías recibir una respuesta personalizada de GPT-3.5

---

## 💰 Costos de la API

### GPT-3.5-turbo (Recomendado):
- **Costo**: ~$0.002 por 1,000 tokens
- **Uso estimado**: ~400 tokens por pregunta
- **Precio por pregunta**: ~$0.0008 (menos de 1 centavo)
- **Con $5 USD**: ~6,250 preguntas

### GPT-4 (Opcional, más inteligente):
- **Costo**: ~$0.03 por 1,000 tokens
- **15x más caro pero más preciso**
- Para usar: cambia `model="gpt-4"` en `services.py`

---

## 🔄 Sistema de Fallback

Si no configuras la API key o hay un error:
- ✅ El asistente seguirá funcionando
- 🤖 Usará sistema basado en reglas (respuestas predefinidas)
- 📊 Seguirá analizando tus datos financieros reales

---

## 🌐 Alternativas a OpenAI

### 1. **Google Gemini** (Tier gratuito generoso)
```python
# En services.py, reemplazar con:
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
```

### 2. **Anthropic Claude**
```python
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
```

### 3. **Groq (Rápido y con tier gratuito)**
```python
from groq import Groq
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
```

---

## 🔒 Seguridad

### ✅ Buenas Prácticas:
- ✅ Nunca subas el archivo `.env` a GitHub
- ✅ `.env` ya está en `.gitignore`
- ✅ No compartas tu API key
- ✅ Rota la key si se expone

### 🚨 Si expones tu key accidentalmente:
1. Ve a https://platform.openai.com/api-keys
2. Revoca la key comprometida inmediatamente
3. Genera una nueva

---

## 📊 Monitoreo de Uso

Ver tu consumo:
- https://platform.openai.com/usage
- Configura límites de gasto mensuales
- Configura alertas de uso

---

## ❓ Troubleshooting

### Error: "Invalid API Key"
- Verifica que la key esté correcta en `.env`
- Asegúrate de que empiece con `sk-`
- Verifica que no haya espacios extras

### Error: "Rate limit exceeded"
- Has superado el límite gratuito
- Espera 1 minuto o agrega créditos

### Error: "Insufficient quota"
- Se acabaron los créditos gratuitos
- Agrega método de pago en OpenAI

### El AI no responde:
- Revisa la consola del backend para errores
- Verifica que el archivo `.env` exista
- El sistema caerá automáticamente al modo basado en reglas

---

## 📚 Recursos Adicionales

- **Documentación OpenAI**: https://platform.openai.com/docs
- **Precios actualizados**: https://openai.com/pricing
- **Ejemplos de uso**: https://platform.openai.com/examples
- **Límites y quotas**: https://platform.openai.com/account/limits

---

## 🎯 Próximos Pasos Opcionales

1. **Historial de conversación persistente**: Guardar chat en DB
2. **Streaming de respuestas**: Ver el texto aparecer palabra por palabra
3. **Análisis de gráficos**: Permitir que la AI analice los gráficos
4. **Voz**: Agregar speech-to-text y text-to-speech
5. **Multi-idioma**: Detectar idioma y responder en consecuencia
