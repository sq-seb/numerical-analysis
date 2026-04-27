# 🚀 GUÍA RÁPIDA DE EJECUCIÓN

## Paso 1: Preparar el Backend

### Abrir Terminal 1 (PowerShell o CMD)
```powershell
cd c:\Users\USUARIO\OneDrive\Documentos\ProyectoAnalisis\numerical-analysis\backend

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar el servidor
```powershell
cd server
python server.py
```

✅ Deberías ver algo como:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## Paso 2: Preparar el Frontend

### Abrir Terminal 2 (Nueva ventana PowerShell)
```powershell
cd c:\Users\USUARIO\OneDrive\Documentos\ProyectoAnalisis\numerical-analysis\frontend

# Instalar dependencias (solo la primera vez)
npm install

# Ejecutar en modo desarrollo
npm run dev
```

✅ Deberías ver algo como:
```
➜  frontend: Local:   http://localhost:5173/
```

---

## Paso 3: Acceder a la Aplicación

Abre tu navegador y ve a: **http://localhost:5173**

---

## 📝 Primer Cálculo de Prueba

### Resolver: x² - 4 = 0

1. **Selecciona**: "Bisección"
2. **Función**: `x**2 - 4`
3. **Intervalo A**: `-5`
4. **Intervalo B**: `5`
5. **Tolerancia**: `0.0001`
6. **Máximo iteraciones**: `100`
7. **Clic en "Calcular"**

**Resultado esperado**: Raíz ≈ 2.0

---

## 🧮 Más Ejemplos

### Ejemplo 2: Función Trigonométrica
- **Método**: Bisección
- **Función**: `math.sin(x) - 0.5`
- **Intervalo A**: `0`
- **Intervalo B**: `1`
- **Resultado**: ≈ 0.5236 (π/6)

### Ejemplo 3: Newton-Raphson
- **Método**: Newton
- **Función**: `x**2 - 4`
- **Punto inicial x0**: `3`
- **Tolerancia**: `0.0001`
- **Resultado**: ≈ 2.0 (muy rápido!)

### Ejemplo 4: Punto Fijo
- **Método**: Punto Fijo
- **Función f(x)**: `x**2 - 4`
- **Función g(x)**: `(4/x)**(0.5)`
- **Punto inicial x0**: `1.5`
- **Resultado**: ≈ 2.0

---

## 🔧 Funciones Disponibles

```python
# Básicas
x**2 - 4              # Parábola
x**3 - 2*x - 5        # Cúbica

# Trigonométricas
math.sin(x)           # Seno
math.cos(x)           # Coseno
math.tan(x)           # Tangente

# Exponenciales
math.exp(x) - 2       # e^x
math.log(x) - 1       # ln(x)

# Combinadas
math.sin(x) - x/2     # Sin(x) - x/2
math.sqrt(x) - 2      # Raíz cuadrada
```

---

## ❓ Solución de Problemas

### Error: "No se puede conectar al servidor"
- [ ] ¿Backend está corriendo en Terminal 1?
- [ ] ¿Puerto 5000 está disponible?
- [ ] Reinicia tanto backend como frontend

### Error: "import Error" en Python
```
pip install sympy
```

### Error: "npm: command not found"
- Instala Node.js desde: https://nodejs.org/
- Reinicia la terminal después

### La aplicación se ve mal
- [ ] Limpia el cache: Ctrl+Shift+Delete
- [ ] Recarga la página: Ctrl+R (o Cmd+R en Mac)
- [ ] Usa un navegador moderno (Chrome, Firefox, Edge)

---

## 📊 Interpretando Resultados

### Tabla de Iteraciones
Muestra para cada iteración:
- `iteration`: Número de iteración
- `approximate_value`: Valor aproximado actual
- `f_evaluated`: f(x) en ese punto
- `error`: Error estimado

### Mensaje de Resultado
- ✓ Verde: Se encontró la raíz
- ⚠ Amarillo: No convergió en el límite

### Raíz Encontrada
Es el valor final que aproxima la raíz de la ecuación

---

## 🎯 Consejos

1. **Para Métodos de Intervalo**: Asegúrate de que f(a) y f(b) tengan signos opuestos
2. **Para Newton**: Usa un punto inicial cercano a la raíz
3. **Para Punto Fijo**: La función g(x) debe converger (|g'(x)| < 1 cerca de la raíz)
4. **Tolerancia**: Valores típicos son 0.0001 o 0.00001
5. **Iteraciones**: 100-1000 es usualmente suficiente

---

## 🎨 Características que Verás

✅ Interfaz moderna con Tailwind CSS
✅ 6 métodos numéricos diferentes
✅ Formularios dinámicos según el método
✅ Tabla de iteraciones interactiva
✅ Manejo robusto de errores
✅ Responsivo en móvil/tablet/desktop

---

## 📚 Notas Matemáticas

### Error Relativo
```
ε = |xₙ₊₁ - xₙ| / |xₙ₊₁|
```

### Error Absoluto
```
ε = |xₙ₊₁ - xₙ|
```

### Criterio de Bisección
```
f(a) × f(b) < 0  →  Existe raíz en [a, b]
```

---

## ✨ ¡Listo para comenzar!

1. Abre Terminal 1 → Backend
2. Abre Terminal 2 → Frontend
3. Abre navegador → http://localhost:5173
4. ¡Selecciona un método y calcula!

**¿Preguntas? Revisa los mensajes de error que aparecen en la interfaz**

---

Última actualización: 2026-04-26
