export function ResultsTable({ data }) {
  if (!data || !data.table || Object.keys(data.table).length === 0) {
    return null
  }

  const columns = Object.keys(data.table[1] || {})

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-700 bg-slate-900/40">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700 bg-slate-800/50">
            {columns.map((col) => (
              <th key={col} className="px-4 py-3 text-left font-semibold text-emerald-300">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Object.entries(data.table).map(([_, row]) => (
            <tr key={_} className="border-b border-slate-800 hover:bg-slate-800/30">
              {columns.map((col) => (
                <td key={col} className="px-4 py-3 text-slate-300">
                  {typeof row[col] === 'number' ? row[col].toFixed(8) : row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
