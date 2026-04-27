import { useState } from "react"
import { ResultsPanel } from "./components/ResultsPanel"

const API_BASE_URL = "http://localhost:5000"

const METHOD_OPTIONS = [
  { value: "bisection", label: "Bisección" },
  { value: "regula-falsi", label: "Regula Falsi" },
  { value: "secant", label: "Secante" },
  { value: "newton", label: "Newton-Raphson" },
  { value: "fixed-point", label: "Punto Fijo" },
  { value: "multiple-roots-2", label: "Raíces Múltiples (2)" },
]

const METHOD_DESCRIPTIONS = {
  "bisection": "Intervalo [a, b] con cambio de signo",
  "regula-falsi": "Intervalo [a, b] con cambio de signo",
  "secant": "Dos puntos iniciales para aproximar la derivada",
  "newton": "Punto inicial x0 y derivada automática",
  "fixed-point": "Punto inicial x0 y función g(x)",
  "multiple-roots-2": "Punto inicial x0 y función f(x) para raíces múltiples",
}

export default function App() {
  const [selectedMethod, setSelectedMethod] = useState("bisection")
  const [functionF, setFunctionF] = useState("x**2 - 4")
  const [functionG, setFunctionG] = useState("x + 1")
  const [intervalA, setIntervalA] = useState("-5")
  const [intervalB, setIntervalB] = useState("5")
  const [x0, setX0] = useState("1.5")
  const [tolerance, setTolerance] = useState("0.0001")
  const [maxIterations, setMaxIterations] = useState("100")
  const [precision, setPrecision] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      let endpoint = ""
      const payload = {
        function_f: functionF,
        tolerance: parseFloat(tolerance),
        max_iterations: parseInt(maxIterations, 10),
        precision,
      }

      switch (selectedMethod) {
        case "bisection":
          endpoint = "/api/bisection"
          Object.assign(payload, {
            interval_a: parseFloat(intervalA),
            interval_b: parseFloat(intervalB),
          })
          break
        case "regula-falsi":
          endpoint = "/api/regula-falsi"
          Object.assign(payload, {
            interval_a: parseFloat(intervalA),
            interval_b: parseFloat(intervalB),
          })
          break
        case "secant":
          endpoint = "/api/secant"
          Object.assign(payload, {
            x0: parseFloat(intervalA),
            interval_b: parseFloat(intervalB),
          })
          break
        case "newton":
          endpoint = "/api/newton"
          Object.assign(payload, {
            x0: parseFloat(x0),
          })
          break
        case "fixed-point":
          endpoint = "/api/fixed-point"
          Object.assign(payload, {
            function_g: functionG,
            x0: parseFloat(x0),
          })
          break
        case "multiple-roots-2":
          endpoint = "/api/multiple-roots-2"
          Object.assign(payload, {
            x0: parseFloat(x0),
          })
          break
        default:
          throw new Error("Método no válido")
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      const data = await response.json()
      if (!response.ok) {
        setError(data.error || "Error en el servidor")
      } else {
        setResults(data)
      }
    } catch (err) {
      setError(`Error de conexión: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const renderMethodFields = () => {
    if (["bisection", "regula-falsi"].includes(selectedMethod)) {
      return (
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-slate-300">Intervalo A</label>
            <input
              type="number"
              value={intervalA}
              onChange={(e) => setIntervalA(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="-5"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300">Intervalo B</label>
            <input
              type="number"
              value={intervalB}
              onChange={(e) => setIntervalB(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="5"
            />
          </div>
        </div>
      )
    }

    if (selectedMethod === "secant") {
      return (
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-slate-300">Punto x0</label>
            <input
              type="number"
              value={intervalA}
              onChange={(e) => setIntervalA(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300">Punto x1</label>
            <input
              type="number"
              value={intervalB}
              onChange={(e) => setIntervalB(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="2"
            />
          </div>
        </div>
      )
    }

    if (["newton", "multiple-roots-2"].includes(selectedMethod)) {
      return (
        <div>
          <label className="block text-sm font-medium text-slate-300">Punto inicial x0</label>
          <input
            type="number"
            value={x0}
            onChange={(e) => setX0(e.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
            placeholder="1.5"
          />
        </div>
      )
    }

    if (selectedMethod === "fixed-point") {
      return (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300">Función g(x)</label>
            <input
              type="text"
              value={functionG}
              onChange={(e) => setFunctionG(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="x + 1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300">Punto inicial x0</label>
            <input
              type="number"
              value={x0}
              onChange={(e) => setX0(e.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
              placeholder="1.5"
            />
          </div>
        </div>
      )
    }

    return null
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-4xl flex-col px-6 py-10 sm:px-10 lg:px-12">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-8 shadow-2xl shadow-slate-950/40">
          <div className="flex flex-col gap-6">
            <div>
              <p className="text-sm uppercase tracking-[0.32em] text-emerald-300">Interfaz simple</p>
              <h1 className="mt-4 text-4xl font-black text-white">Calcula raíces numéricas</h1>
              <p className="mt-3 text-slate-400">Escribe la función, elige el método y presiona calcular. Verás el error y la tabla de iteraciones.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-3">
                <label className="block text-sm font-medium text-slate-300">Función f(x)</label>
                <input
                  type="text"
                  value={functionF}
                  onChange={(e) => setFunctionF(e.target.value)}
                  placeholder="Ej: x**2 - 4, sin(x), sen(x), cos(x), e**x"
                  className="w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white placeholder-slate-500"
                />
                <p className="mt-2 text-xs text-slate-500">Usa `sin`, `sen`, `cos`, `tan`, `exp`, `ln`, `e`, `pi`, y `^` como potencia.</p>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-slate-300">Método</label>
                  <select
                    value={selectedMethod}
                    onChange={(e) => setSelectedMethod(e.target.value)}
                    className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
                  >
                    {METHOD_OPTIONS.map((method) => (
                      <option key={method.value} value={method.value}>{method.label}</option>
                    ))}
                  </select>
                </div>
                <div className="flex items-end">
                  <button
                    type="submit"
                    className="w-full rounded-2xl bg-emerald-500 px-6 py-3 text-base font-semibold text-slate-950 transition hover:bg-emerald-400"
                  >
                    Calcular
                  </button>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-700 bg-slate-950/70 p-5">
                <p className="text-sm text-slate-400">Descripción del método:</p>
                <p className="mt-2 text-white">{METHOD_DESCRIPTIONS[selectedMethod]}</p>
              </div>

              {renderMethodFields()}

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-slate-300">Tolerancia</label>
                  <input
                    type="number"
                    value={tolerance}
                    onChange={(e) => setTolerance(e.target.value)}
                    className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
                    step="0.00001"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300">Máximo iteraciones</label>
                  <input
                    type="number"
                    value={maxIterations}
                    onChange={(e) => setMaxIterations(e.target.value)}
                    className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-white"
                  />
                </div>
              </div>

              <div className="flex items-center gap-3">
                <input
                  id="precision"
                  type="checkbox"
                  checked={precision}
                  onChange={(e) => setPrecision(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-700 bg-slate-950/50 accent-emerald-500"
                />
                <label htmlFor="precision" className="text-sm text-slate-300">
                  Usar precisión absoluta
                </label>
              </div>
            </form>
          </div>
        </div>

        <div className="mt-8">
          <ResultsPanel data={results} error={error} loading={loading} />
        </div>
      </div>
    </main>
  )
}
