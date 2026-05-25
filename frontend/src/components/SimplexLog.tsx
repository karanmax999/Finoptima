import React, { useState } from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { ChevronLeft, ChevronRight, CornerDownRight } from 'lucide-react';

export const SimplexLog: React.FC = () => {
  const { apiResults } = useFinoptimaStore();
  const [selectedStep, setSelectedStep] = useState(0);

  const diagnostics = apiResults?.simplex_diagnostics;
  if (!diagnostics || !diagnostics.iterations || diagnostics.iterations.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl font-mono text-xs text-slate-500 py-16 text-center">
        Awaiting simplex LPP solver iterations...
      </div>
    );
  }

  const iterations = diagnostics.iterations;
  const currentIter = iterations[selectedStep] || iterations[0];
  const tableau = currentIter.tableau;
  const pivot = currentIter.pivot;

  const handlePrev = () => {
    setSelectedStep(prev => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    setSelectedStep(prev => Math.min(iterations.length - 1, prev + 1));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl font-mono text-left">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-800 pb-3 mb-4 gap-2">
        <div className="flex items-center gap-2">
          <span className="text-emerald-400 font-bold uppercase tracking-wider text-xs">
            🎚️ Simplex Tableau Diagnostics
          </span>
          <span className="bg-emerald-950 text-emerald-400 text-xxs px-2.5 py-0.5 rounded-full border border-emerald-900/60 font-semibold uppercase">
            Status: {diagnostics.solver_status}
          </span>
        </div>

        {/* Stepper buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handlePrev}
            disabled={selectedStep === 0}
            className="p-1 rounded bg-slate-950 border border-slate-800 hover:border-slate-700/80 transition-colors disabled:opacity-40 disabled:cursor-not-allowed text-slate-300"
          >
            <ChevronLeft size={16} />
          </button>
          <span className="text-xxs font-mono text-slate-400">
            Iter: <span className="text-cyan-400 font-bold">{selectedStep}</span> / {iterations.length - 1}
          </span>
          <button
            onClick={handleNext}
            disabled={selectedStep === iterations.length - 1}
            className="p-1 rounded bg-slate-950 border border-slate-800 hover:border-slate-700/80 transition-colors disabled:opacity-40 disabled:cursor-not-allowed text-slate-300"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

      {/* Step explanation */}
      <div className="p-3 bg-slate-950/60 border border-slate-850 rounded-lg mb-4 text-xxs leading-normal text-slate-300">
        <div className="flex items-start gap-2">
          <CornerDownRight size={12} className="text-cyan-400 shrink-0 mt-0.5" />
          <div>
            <span className="text-cyan-400 font-semibold block uppercase text-xxs tracking-wider mb-0.5">
              Iteration Step {currentIter.step} Details
            </span>
            <p className="text-slate-300">{currentIter.message}</p>
          </div>
        </div>
      </div>

      {/* Exact simplex tableau table */}
      <div className="overflow-x-auto border border-slate-800 rounded-lg bg-slate-950/40">
        <table className="w-full text-left border-collapse text-xxs">
          <thead>
            <tr className="border-b border-slate-850 bg-slate-950 text-slate-500">
              <th className="p-2 border-r border-slate-850">Basis</th>
              {tableau.headers.map((h, idx) => {
                const isPivotCol = pivot && idx === pivot.pivot_col;
                return (
                  <th
                    key={h}
                    className={`p-2 border-r border-slate-850 text-right font-bold ${isPivotCol ? 'text-amber-400 bg-amber-950/20' : ''}`}
                  >
                    {h}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {tableau.matrix.map((row, rIdx) => {
              const isObjRow = rIdx === tableau.matrix.length - 1;
              const isPivotRow = pivot && rIdx === pivot.pivot_row;
              const rowName = tableau.row_names[rIdx] || (isObjRow ? "z" : `Row ${rIdx}`);
              
              return (
                <tr
                  key={rIdx}
                  className={`border-b border-slate-850 hover:bg-slate-900/30 transition-colors ${
                    isObjRow ? 'bg-slate-950 text-slate-300 font-bold border-t border-slate-800' : 'text-slate-400'
                  } ${isPivotRow ? 'bg-cyan-950/15' : ''}`}
                >
                  <td className="p-2 border-r border-slate-850 font-semibold text-slate-500 whitespace-nowrap">
                    {rowName.split('(')[0]}
                    {rowName.includes('(') && (
                      <span className="text-xxs text-cyan-500/80 font-normal">
                        ({rowName.split('(')[1]}
                      </span>
                    )}
                  </td>
                  {row.map((val, cIdx) => {
                    const isPivotCol = pivot && cIdx === pivot.pivot_col;
                    const isPivotCell = pivot && rIdx === pivot.pivot_row && cIdx === pivot.pivot_col;
                    return (
                      <td
                        key={cIdx}
                        className={`p-2 border-r border-slate-850 text-right font-mono ${
                          isPivotCell
                            ? 'bg-amber-500/25 border-2 border-amber-500 text-amber-300 font-bold'
                            : isPivotCol
                            ? 'bg-amber-950/10 text-amber-200'
                            : isPivotRow
                            ? 'text-cyan-300'
                            : isObjRow && cIdx === row.length - 1
                            ? 'text-emerald-400 font-bold font-display text-xs'
                            : ''
                        }`}
                      >
                        {val.toFixed(4)}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pivot statistics summaries */}
      {pivot && (
        <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950/40 p-3 rounded-lg border border-slate-850 text-xxs">
          <div>
            <span className="text-slate-500 block uppercase tracking-wider mb-0.5">Entering Variable</span>
            <span className="text-amber-400 font-bold">{pivot.entering_var}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase tracking-wider mb-0.5">Leaving Variable</span>
            <span className="text-cyan-400 font-bold">{pivot.leaving_var}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase tracking-wider mb-0.5">Pivot Value (&theta;)</span>
            <span className="text-amber-300 font-mono">{pivot.pivot_value.toFixed(4)}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase tracking-wider mb-0.5">Current Objective</span>
            <span className="text-emerald-400 font-bold">{(tableau.objective_value * 100).toFixed(3)}%</span>
          </div>
        </div>
      )}
    </div>
  );
};
export default SimplexLog;
