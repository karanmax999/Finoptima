import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { Terminal, AlertCircle } from 'lucide-react';

export const RegressionDiagnostics: React.FC = () => {
  const { apiResults } = useFinoptimaStore();
  const reg = apiResults?.regression_diagnostics;

  if (!reg) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl font-mono text-left">
      <div className="flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
        <h3 className="text-cyan-400 font-bold uppercase tracking-wider text-xs flex items-center gap-2">
          <Terminal size={14} /> Multiple Linear Regression Diagnostics
        </h3>
        <span className="bg-cyan-950/30 text-cyan-400 text-xxs px-2.5 py-0.5 rounded-full border border-cyan-900/60 font-semibold uppercase">
          Alpha Factors Fit
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xxs text-slate-300">
        {/* Regression summary statistics */}
        <div className="space-y-3">
          <p className="font-bold text-slate-400 uppercase text-xxs tracking-wider">I. Model Fit Summary</p>
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-850/80 space-y-2">
            <div className="flex justify-between border-b border-slate-900 pb-1.5">
              <span className="text-slate-500">R-Squared (R&sup2;):</span>
              <span className="text-emerald-400 font-bold">{reg.r_squared.toFixed(5)}</span>
            </div>
            <div className="flex justify-between border-b border-slate-900 pb-1.5">
              <span className="text-slate-500">Adjusted R-Squared:</span>
              <span className="text-emerald-400 font-bold">{reg.adjusted_r_squared.toFixed(5)}</span>
            </div>
            <div className="flex justify-between border-b border-slate-900 pb-1.5">
              <span className="text-slate-500">Root Mean Squared Error (RMSE):</span>
              <span className="text-cyan-300">{reg.rmse.toFixed(6)}</span>
            </div>
            <div className="flex justify-between border-b border-slate-900 pb-1.5">
              <span className="text-slate-500">Mean Absolute Error (MAE):</span>
              <span className="text-cyan-300">{reg.mae.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Model Intercept (&alpha;):</span>
              <span className="text-indigo-400 font-bold">{reg.intercept.toFixed(6)}</span>
            </div>
          </div>
        </div>

        {/* Feature coefficients and significance tables */}
        <div className="space-y-3">
          <p className="font-bold text-slate-400 uppercase text-xxs tracking-wider">II. Coefficients & Statistical Significance</p>
          <div className="border border-slate-850 rounded-xl overflow-hidden bg-slate-950/40">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-850 bg-slate-950 text-slate-500">
                  <th className="p-2">Independent Factor</th>
                  <th className="p-2 text-right">Coefficient (&beta;)</th>
                  <th className="p-2 text-right">p-value</th>
                  <th className="p-2 text-center">Significance</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(reg.coefficients).map(([factor, coef]) => {
                  const pVal = reg.p_values[factor] ?? 0.05;
                  const isSignificant = pVal < 0.05;
                  return (
                    <tr key={factor} className="border-b border-slate-850 hover:bg-slate-900/10">
                      <td className="p-2 font-semibold text-slate-400">{factor}</td>
                      <td className="p-2 text-right text-cyan-400 font-mono">{coef.toFixed(5)}</td>
                      <td className={`p-2 text-right font-mono ${isSignificant ? 'text-emerald-400 font-bold' : 'text-rose-400'}`}>
                        {pVal < 0.001 ? '< 0.001' : pVal.toFixed(4)}
                      </td>
                      <td className="p-2 text-center">
                        {isSignificant ? (
                          <span className="bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-900/60 font-bold text-[9px]">
                            SIGNIFICANT
                          </span>
                        ) : (
                          <span className="bg-rose-950/40 text-rose-400 px-2 py-0.5 rounded border border-rose-900/40 font-bold text-[9px] flex items-center justify-center gap-0.5">
                            <AlertCircle size={9} /> WEAK
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
export default RegressionDiagnostics;
