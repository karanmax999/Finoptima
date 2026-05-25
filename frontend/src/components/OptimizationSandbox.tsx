import React, { useEffect } from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { Sliders, Settings, DollarSign, Loader2 } from 'lucide-react';

export const OptimizationSandbox: React.FC = () => {
  const store = useFinoptimaStore();

  const handleSliderChange = (type: 'return' | 'concentration', value: number) => {
    if (type === 'return') {
      store.setLppConstraints(value, store.maxConcentration);
    } else {
      store.setLppConstraints(store.minReturnConstraint, value);
    }
  };

  useEffect(() => {
    // Throttle backend optimization calls to 200ms
    const timeout = setTimeout(() => {
      store.fetchOptimization();
    }, 200);
    return () => clearTimeout(timeout);
  }, [store.minReturnConstraint, store.maxConcentration, store.tickers]);

  const lpData = store.apiResults?.linear_programming;
  const expectedReturns = store.apiResults?.expected_returns ?? [];
  const tickers = store.apiResults?.tickers ?? [];

  return (
    <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-6 rounded-2xl flex flex-col justify-between h-full">
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
            <Sliders size={14} className="text-emerald-400" /> LPP Optimization Sandbox
          </h3>
          <span className="text-slate-500 font-mono text-xxs flex items-center gap-1">
            {store.isCalculating ? (
              <Loader2 size={12} className="animate-spin text-emerald-400" />
            ) : (
              <Settings size={12} className="text-emerald-400" />
            )}
            Solver: PuLP Simplex
          </span>
        </div>

        <div className="space-y-4">
          {/* Minimum return constraint */}
          <div>
            <div className="flex justify-between text-xxs font-mono text-slate-400 uppercase tracking-wider mb-1.5">
              <span>Minimum Target Return (R_min):</span>
              <span className="text-emerald-400 font-bold">{(store.minReturnConstraint * 100).toFixed(2)}%</span>
            </div>
            <input
              type="range"
              min="0.00"
              max="0.15"
              step="0.005"
              value={store.minReturnConstraint}
              onChange={(e) => handleSliderChange('return', parseFloat(e.target.value))}
              className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
            />
          </div>

          {/* Maximum concentration cap */}
          <div>
            <div className="flex justify-between text-xxs font-mono text-slate-400 uppercase tracking-wider mb-1.5">
              <span>Maximum Asset Weight Cap (c):</span>
              <span className="text-cyan-400 font-bold">{(store.maxConcentration * 100).toFixed(1)}%</span>
            </div>
            <input
              type="range"
              min="0.10"
              max="1.00"
              step="0.05"
              value={store.maxConcentration}
              onChange={(e) => handleSliderChange('concentration', parseFloat(e.target.value))}
              className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
            />
          </div>
        </div>

        {/* solver status and returns */}
        {lpData && (
          <div className="mt-5 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-slate-500 font-mono text-xxs uppercase tracking-wider block">Constrained LP Portfolio Return</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold font-display text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
                  {(lpData.return * 100).toFixed(3)}%
                </span>
                <span className="text-xxs font-mono text-slate-400">
                  (R_min: {(store.minReturnConstraint * 100).toFixed(1)}%)
                </span>
              </div>
            </div>
            <div className="flex items-center gap-1 bg-slate-900 border border-slate-800/60 rounded-full px-2.5 py-1">
              <div className={`w-2 h-2 rounded-full ${lpData.status === 'Optimal' || lpData.status === '1' ? 'bg-emerald-500' : 'bg-rose-500'}`} />
              <span className="text-xxs font-mono text-slate-300 font-semibold uppercase">
                {lpData.status === '1' || lpData.status === 'Optimal' ? 'Optimal' : lpData.status}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* allocations lists */}
      {lpData && (
        <div className="mt-4 border-t border-slate-800/80 pt-4">
          <span className="text-slate-500 font-mono text-xxs uppercase tracking-wider block mb-2 flex items-center gap-1">
            <DollarSign size={12} className="text-emerald-400" /> Optimal Weight Allocations
          </span>
          <div className="grid grid-cols-2 gap-3">
            {tickers.map((ticker, idx) => {
              const weight = lpData.weights[ticker] ?? 0.0;
              const ret = expectedReturns[idx] ?? 0.0;
              return (
                <div key={ticker} className="bg-slate-950/40 p-2.5 rounded border border-slate-850 flex justify-between items-center">
                  <div>
                    <span className="font-bold text-xs text-slate-300 block">{ticker}</span>
                    <span className="text-slate-500 text-xxs font-mono">Ret: {(ret * 100).toFixed(2)}%</span>
                  </div>
                  <span className="text-cyan-400 font-mono font-bold text-sm">
                    {(weight * 100).toFixed(1)}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
export default OptimizationSandbox;
