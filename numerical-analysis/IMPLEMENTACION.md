# Resumen de Implementación - Métodos Numéricos

## ✅ Completado

### Backend - Python/Flask

#### Estructura de Directorios
```
backend/server/
├── server.py                          # Servidor principal con 6 endpoints
├── numerical/
│   ├── interfaces/
│   │   ├── interval_method.py        # clase base IntervalMethod
│   │   └── iterative_method.py       # Clase base IterativeMethod
│   └── services/
│       ├── bisection_service.py      # Implementación Bisección
│       ├── regula_falsi_service.py   # Implementación Regula Falsi
│       ├── secant_service.py         # Implementación Secante
│       ├── newton_service.py         # Implementación Newton-Raphson
│       ├── fixed_point_service.py    # Implementación Punto Fijo
│       └── multiple_roots_2_service.py # Implementación Raíces Múltiples
├── shared/utils/
│   ├── plot_function.py              # Utilidad para gráficas
│   └── convert_math_to_simply.py     # Conversión de sintaxis matemática
```

#### Endpoints API
- **POST /api/bisection** - Resuelve ecuaciones por Bisección
- **POST /api/regula-falsi** - Resuelve ecuaciones por Regula Falsi
- **POST /api/secant** - Resuelve ecuaciones por Secante
- **POST /api/newton** - Resuelve ecuaciones por Newton-Raphson
- **POST /api/fixed-point** - Resuelve ecuaciones por Punto Fijo
- **POST /api/multiple-roots-2** - Resuelve ecuaciones con raíces múltiples

#### Características Backend
✓ Validación de entrada en ambos lados
✓ Manejo de errores robusto
✓ Cálculo automático de derivadas con SymPy
✓ Soporte para precisión absoluta y relativa
✓ Retorno de tabla de iteraciones completa
✓ CORS habilitado para desarrollo

### Frontend - React/Tailwind

#### Componentes React
```
frontend/src/
├── App.jsx                           # Componente principal
├── components/
│   ├── MethodSelector.jsx            # Selector de 6 métodos
│   ├── IntervalMethodForm.jsx        # Formulario para métodos de intervalo
│   ├── IterativeMethodForm.jsx       # Formulario para métodos iterativos
│   ├── ResultsPanel.jsx              # Panel de resultados con tabla
│   └── InputField.jsx                # Campo de entrada reutilizable
├── index.css                         # Estilos globales con Tailwind
└── main.jsx                          # Punto de entrada
```

#### Características Frontend
✓ Interfaz moderna con Tailwind CSS v4
✓ Selección visual de método
✓ Formularios dinámicos según el método
✓ Validación de entrada en cliente
✓ Visualización de tabla de iteraciones
✓ Manejo de estados de carga/error
✓ Diseño responsivo (móvil, tablet, desktop)
✓ Layout de dos columnas: formulario + resultados
✓ Animaciones suaves y transiciones

## 🚀 Cómo Iniciar

### 1. Instalar Dependencias

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### 2. Ejecutar los Servidores

#### Terminal 1 - Backend
```bash
cd backend/server
python server.py
# Servidor en http://localhost:5000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
# Aplicación en http://localhost:5173
```

## 📊 Métodos Implementados

### Métodos de Intervalo (Requieren cambio de signo)

**Bisección**
- Más simple y robusto
- Convergencia lenta pero garantizada
- No requiere derivadas

**Regula Falsi**
- Mejora de bisección
- Usa interpolación lineal
- Convergencia más rápida

**Secante**
- Aproxima derivada numéricamente
- No requiere calcular derivada analítica
- Convergencia superlineal

### Métodos Iterativos (Requieren punto inicial)

**Newton-Raphson**
- Muy rápido (convergencia cuadrática)
- Requiere calcular derivada
- Puede divergir si x₀ está lejano

**Punto Fijo**
- Reformula f(x)=0 como x=g(x)
- Flexibilidad en elegir g(x)
- Convergencia lineal

**Raíces Múltiples**
- Especializado para raíces repetidas
- Usa primera y segunda derivada
- Mantiene convergencia cuadrática

## 📝 Ejemplos de Uso

### Ecuación: x² - 4 = 0
- **Función**: `x**2 - 4`
- **Por Bisección**: Intervalo [-5, 5]
- **Por Newton**: Punto inicial x₀ = 3
- **Raíz esperada**: ±2

### Ecuación: sin(x) - 0.5 = 0
- **Función**: `math.sin(x) - 0.5`
- **Por Bisección**: Intervalo [0, 1]
- **Raíz esperada**: π/6 ≈ 0.524

### Ecuación: Punto Fijo
- **Función**: `x**2 - 4`
- **g(x)**: `(4/x)**(0.5)` o similar
- **Punto inicial**: x₀ = 1

## 🔧 Requisitos Técnicos

### Backend
- Python 3.8+
- Flask 3.1+
- SymPy 1.13
- NumPy 2.4+
- Pandas 3.0+
- Flask-CORS 6.0+

### Frontend
- Node.js 16+
- React 19.2+
- Tailwind CSS 4.2+
- Vite 8.0+

## 📌 Notas Importantes

1. **Sintaxis de Funciones**
   - Usa `x` como variable
   - Usa `**` para potencias
   - Funciones: `math.sin()`, `math.cos()`, `math.sqrt()`, `math.exp()`, `math.log()`

2. **Validaciones**
   - Intervalo debe tener cambio de signo para métodos de intervalo
   - Tolerancia debe ser positiva
   - El máximo de iteraciones previene bucles infinitos

3. **Precisión**
   - Por defecto: precisión relativa
   - Opcional: precisión absoluta

4. **Resultados**
   - Se devuelve tabla completa de iteraciones
   - Se incluye el valor final de la raíz encontrada
   - Se muestran advertencias si existen

## 🎨 Características del Diseño

- Paleta de colores: slate-950 (fondos) + emerald-500 (acentos)
- Componentes redondeados (border-radius 2xl)
- Bordes suaves con backdrop blur
- Animaciones y transiciones suaves
- Tipografía clara y legible
- Layout responsivo con Tailwind grid
- Card-based design pattern
- Dark mode como tema principal

## 📚 Referencia de Componentes

### MethodSelector
Muestra 6 botones para seleccionar el método numérico con descripción.

### IntervalMethodForm
Formulario con campos para:
- function_f
- interval_a, interval_b
- tolerance, max_iterations
- precision checkbox

### IterativeMethodForm
Formulario con campos para:
- function_f (y function_g si es Punto Fijo)
- x0
- tolerance, max_iterations
- precision checkbox

### ResultsPanel
Muestra:
- Mensaje de resultado
- Raíz encontrada (en card destacada)
- Tabla de iteraciones scrolleable
- Advertencias si las hay
- Estado de carga animado
- Errores en rojo

## 🐛 Troubleshooting

### "CORS Error"
→ Verifica que backend está corriendo en puerto 5000

### "No se puede conectar al servidor"
→ Comprueba que ambos están ejecutándose

### "División por cero"
→ Cambia intervalo o punto inicial

### "No converge"
→ Aumenta iteraciones o cambia parámetros

## 📋 Próximas Mejoras Posibles

- [ ] Agregar visualización gráfica de funciones
- [ ] Exportar resultados a PDF
- [ ] Historial de cálculos
- [ ] Comparación entre métodos
- [ ] Soporte para sistemas de ecuaciones
- [ ] Editor visual de funciones
- [ ] Más métodos numéricos

---

**Proyecto completado: 2026-04-26**
