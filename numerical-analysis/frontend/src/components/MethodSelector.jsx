import { useState } from 'react'

export function MethodSelector({ onMethodSelect }) {
  const methods = [
    {
      id: 'bisection',
      name: 'Bisección',
      description: 'Divide el intervalo por la mitad iterativamente'
    },
    {
      id: 'regula-falsi',
      name: 'Regula Falsi',
      description: 'Localiza raíces usando interpolación lineal'
    },
    {
      id: 'secant',
      name: 'Secante',
      description: 'Aproxima la derivada usando dos puntos'
    },
    {
      id: 'newton',
      name: 'Newton-Raphson',
      description: 'Utiliza la derivada para encontrar raíces'
    },
    {
      id: 'fixed-point',
      name: 'Punto Fijo',
      description: 'Reformula la ecuación en forma x = g(x)'
    },
    {
      id: 'multiple-roots-2',
      name: 'Raíces Múltiples (2)',
      description: 'Para ecuaciones con raíces múltiples'
    },
  ]

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-white">Selecciona un Método</h2>
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {methods.map((method) => (
          <button
            key={method.id}
            onClick={() => onMethodSelect(method.id)}
            className="rounded-2xl border border-slate-700 bg-slate-900/60 p-4 text-left transition hover:border-emerald-500 hover:bg-slate-800"
          >
            <h3 className="font-semibold text-emerald-300">{method.name}</h3>
            <p className="mt-1 text-sm text-slate-400">{method.description}</p>
          </button>
        ))}
      </div>
    </div>
  )
}
