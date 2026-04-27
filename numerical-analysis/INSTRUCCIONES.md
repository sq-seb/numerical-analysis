# Instrucciones para ejecutar el proyecto

## Backend

### Instalación de dependencias
```bash
cd backend
pip install -r requirements.txt
```

### Ejecutar el servidor
```bash
cd backend/server
python server.py
```

El servidor estará disponible en `http://localhost:5000`

### Endpoints disponibles

- **POST /api/bisection** - Método de Bisección
- **POST /api/secant** - Método de Secante
- **POST /api/regula-falsi** - Método de Regula Falsi
- **POST /api/newton** - Método de Newton-Raphson
- **POST /api/fixed-point** - Método de Punto Fijo
- **POST /api/multiple-roots-2** - Método de Raíces Múltiples (2)

## Frontend

### Instalación de dependencias
```bash
cd frontend
npm install
```

### Ejecutar en desarrollo
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

### Construir para producción
```bash
npm run build
```

## Ejemplos de funciones

- `x**2 - 4` - Parábola
- `math.sin(x) - 0.5` - Función seno
- `math.exp(x) - 2` - Exponencial
- `x**3 - 2*x - 5` - Cúbica
- `math.log(x) - 1` - Logaritmo natural

## Notas importantes

1. Las funciones deben usar sintaxis de Python con `math.` para funciones matemáticas
2. Use `x` como variable independiente
3. Los exponentes se escriben con `**`
4. La tolerancia es el criterio de parada (error máximo permitido)
5. El máximo de iteraciones previene bucles infinitos

## Métodos disponibles

### Métodos de Intervalo (requieren cambio de signo)
- **Bisección**: La más simple pero más lenta
- **Regula Falsi**: Mejora de bisección con interpolación
- **Secante**: Aproxima la derivada sin calcularla

### Métodos Iterativos (requieren punto inicial)
- **Newton-Raphson**: Rápido pero requiere la derivada
- **Punto Fijo**: Reformula la ecuación como x = g(x)
- **Raíces Múltiples**: Para ecuaciones con raíces repetidas
