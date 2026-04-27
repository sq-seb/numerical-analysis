import { InputField } from './InputField'

export function IntervalMethodForm({ 
  onSubmit, 
  loading = false,
  methodName = 'Método de Intervalo'
}) {
  const [formData, setFormData] = React.useState({
    function_f: 'x**2 - 4',
    interval_a: '-5',
    interval_b: '5',
    tolerance: '0.0001',
    max_iterations: '100',
    precision: false,
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="rounded-2xl border border-slate-700 bg-slate-900/40 p-6">
        <h3 className="mb-4 text-lg font-semibold text-white">{methodName}</h3>
        
        <div className="space-y-4">
          <InputField
            label="Función f(x)"
            name="function_f"
            value={formData.function_f}
            onChange={handleChange}
            placeholder="Ej: x**2 - 4, math.sin(x), math.exp(x)"
            required
          />
          
          <div className="grid gap-4 md:grid-cols-2">
            <InputField
              label="Intervalo A"
              name="interval_a"
              type="number"
              value={formData.interval_a}
              onChange={handleChange}
              step="0.01"
              required
            />
            <InputField
              label="Intervalo B"
              name="interval_b"
              type="number"
              value={formData.interval_b}
              onChange={handleChange}
              step="0.01"
              required
            />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <InputField
              label="Tolerancia"
              name="tolerance"
              type="number"
              value={formData.tolerance}
              onChange={handleChange}
              step="0.00001"
              required
            />
            <InputField
              label="Máximo de iteraciones"
              name="max_iterations"
              type="number"
              value={formData.max_iterations}
              onChange={handleChange}
              required
            />
          </div>

          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="precision"
              name="precision"
              checked={formData.precision}
              onChange={handleChange}
              className="h-4 w-4 rounded border-slate-700 bg-slate-950/50 accent-emerald-500"
            />
            <label htmlFor="precision" className="text-sm text-slate-300">
              Usar precisión absoluta (por defecto: relativa)
            </label>
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-xl bg-emerald-500/20 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-emerald-500/30 disabled:opacity-50"
      >
        {loading ? 'Calculando...' : 'Calcular'}
      </button>
    </form>
  )
}
