export function ResultsPanel({ data, error, loading }) {
  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-700 bg-slate-900/40 p-8 text-center">
        <div className="inline-block animate-spin rounded-full border-4 border-slate-700 border-t-emerald-500 h-8 w-8"></div>
        <p className="mt-4 text-slate-300">Calculando...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-2xl border-l-4 border-l-red-500 border border-slate-700 bg-red-950/20 p-6">
        <h3 className="font-semibold text-red-400">Error</h3>
        <p className="mt-2 text-red-300">{error}</p>
      </div>
    )
  }

  if (!data) {
    return null
  }

  const success = data.have_solution ? 'text-emerald-400' : 'text-yellow-400'
  const icon = data.have_solution ? '✓' : '⚠'

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-700 bg-slate-900/40 p-6">
        <div className={`flex items-center space-x-3 ${success}`}>
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-lg">{data.message_method}</h3>
        </div>
        
        {data.have_solution && (
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div className="rounded-lg bg-slate-800/50 p-4">
              <p className="text-sm text-slate-400">Raíz encontrada</p>
              <p className="mt-2 text-2xl font-bold text-emerald-300">{data.root?.toFixed(8)}</p>
            </div>
            {data.warnings && data.warnings.length > 0 && (
              <div className="rounded-lg bg-yellow-950/30 p-4">
                <p className="text-sm text-yellow-300">Advertencias:</p>
                <ul className="mt-2 space-y-1 text-sm text-yellow-200">
                  {data.warnings.map((warn, i) => (
                    <li key={i}>• {warn}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {data.table && Object.keys(data.table).length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-white">Tabla de iteraciones</h3>
          <div className="overflow-x-auto rounded-2xl border border-slate-700 bg-slate-900/40">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700 bg-slate-800/50">
                  {Object.keys(data.table[1] || {}).map((col) => (
                    <th key={col} className="px-4 py-3 text-left font-semibold text-emerald-300">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.entries(data.table).map(([_, row]) => (
                  <tr key={_} className="border-b border-slate-800 hover:bg-slate-800/30">
                    {Object.values(row).map((val, i) => (
                      <td key={i} className="px-4 py-3 text-slate-300 font-mono text-xs">
                        {typeof val === 'number' ? val.toFixed(8) : val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
