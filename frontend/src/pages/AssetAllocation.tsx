import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

export const AssetAllocation: React.FC = () => {
  const store = useFinoptimaStore();
  const markowitz = store.apiResults?.markowitz;
  const currentReturn = (markowitz?.max_sharpe.return || 0.0842) * 100;
  const currentVol = (markowitz?.max_sharpe.volatility || 0.1105) * 100;
  const sharpe = markowitz?.max_sharpe.sharpe_ratio || 1.24;

  return (
    <div className="p-6 md:p-10">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:justify-between md:items-end mb-10 gap-4">
        <div>
          <div className="flex items-center gap-2 text-on-surface-variant mb-2">
            <span className="font-body text-xs font-semibold tracking-wider uppercase text-primary">Module 4</span>
            <span className="w-1 h-1 rounded-full bg-outline-variant"></span>
            <span className="font-body text-xs font-medium">Execution Engine</span>
          </div>
          <h1 className="font-headline text-4xl md:text-5xl font-bold text-on-surface leading-tight tracking-tight">Optimal Asset Allocation Workbench</h1>
          <p className="font-body text-base text-on-surface-variant mt-2 max-w-2xl">Translating complex statistical findings into actionable capital deployment strategies across multi-asset portfolios.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-5 py-2.5 border border-outline-variant text-on-surface font-body font-semibold text-sm rounded-lg hover:border-primary hover:text-primary transition-all flex items-center gap-2">
            <span className="material-symbols-outlined text-sm">download</span>
            Export IPS
          </button>
          <button className="px-5 py-2.5 bg-primary text-on-primary font-body font-semibold text-sm rounded-lg hover:bg-primary/90 transition-all shadow-sahara-soft flex items-center gap-2">
            <span className="material-symbols-outlined text-sm">play_arrow</span>
            Execute Trades
          </button>
        </div>
      </div>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 lg:gap-8">
        
        {/* Execution Summary (Top spanning) */}
        <div className="xl:col-span-12 bg-surface-container-lowest rounded-xl p-6 lg:p-8 border border-outline-variant/40 shadow-sahara-soft relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-headline text-2xl font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">insights</span>
              Optimization Summary
            </h2>
            <span className="px-3 py-1 bg-surface-variant text-on-surface font-body text-xs font-semibold rounded-full border border-outline-variant/60">Target: Global Balanced</span>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 relative z-10">
            <div className="border-l-2 border-primary/30 pl-4">
              <p className="font-body text-sm text-on-surface-variant mb-1">Expected Return (Ann.)</p>
              <p className="font-headline text-3xl font-bold text-on-surface">{currentReturn.toFixed(2)}% <span className="text-sm font-body text-primary font-medium ml-1">+1.2%</span></p>
            </div>
            <div className="border-l-2 border-outline-variant pl-4">
              <p className="font-body text-sm text-on-surface-variant mb-1">Portfolio Volatility</p>
              <p className="font-headline text-3xl font-bold text-on-surface">{currentVol.toFixed(2)}% <span className="text-sm font-body text-secondary font-medium ml-1">-0.4%</span></p>
            </div>
            <div className="border-l-2 border-outline-variant pl-4">
              <p className="font-body text-sm text-on-surface-variant mb-1">Sharpe Ratio</p>
              <p className="font-headline text-3xl font-bold text-on-surface">{sharpe.toFixed(2)} <span className="text-sm font-body text-primary font-medium ml-1">+0.15</span></p>
            </div>
            <div className="border-l-2 border-outline-variant pl-4">
              <p className="font-body text-sm text-on-surface-variant mb-1">Max Drawdown (Est)</p>
              <p className="font-headline text-3xl font-bold text-on-surface">14.2%</p>
            </div>
          </div>
        </div>

        {/* Left Column: Math & Constraints */}
        <div className="xl:col-span-5 flex flex-col gap-6 lg:gap-8">
          {/* LPP Formulation Workspace */}
          <div className="bg-surface-container-low rounded-xl p-6 border border-outline-variant/60 shadow-sahara-soft flex-1">
            <div className="flex justify-between items-center mb-5">
              <h3 className="font-headline text-xl font-bold text-on-surface">Formulation Workspace</h3>
              <button className="text-on-surface-variant hover:text-primary transition-colors"><span className="material-symbols-outlined text-sm">edit</span></button>
            </div>
            <div className="space-y-6">
              {/* Objective */}
              <div>
                <p className="font-body text-xs font-semibold text-tertiary tracking-wider uppercase mb-2">Objective Function</p>
                <div className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/40 font-mono text-sm text-on-surface">
                  <span className="text-primary font-bold">Maximize:</span> ∑ (w<sub>i</sub> × E[R<sub>i</sub>])
                </div>
              </div>
              {/* Constraints */}
              <div>
                <p className="font-body text-xs font-semibold text-secondary tracking-wider uppercase mb-2">Active Constraints (Basel III Aligned)</p>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-3 bg-surface-container-lowest rounded border border-outline-variant/20 cursor-default">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-secondary text-sm">check_circle</span>
                      <span className="font-body text-sm font-medium">Budget Constraint</span>
                    </div>
                    <span className="font-mono text-xs text-on-surface-variant">∑ w<sub>i</sub> = 1</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-surface-container-lowest rounded border border-outline-variant/20 cursor-default">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-secondary text-sm">check_circle</span>
                      <span className="font-body text-sm font-medium">Long-Only Restriction</span>
                    </div>
                    <span className="font-mono text-xs text-on-surface-variant">w<sub>i</sub> ≥ 0</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-surface-container-lowest rounded border border-outline-variant/20 cursor-default">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-secondary text-sm">check_circle</span>
                      <span className="font-body text-sm font-medium">Max VaR (99%, 10d)</span>
                    </div>
                    <span className="font-mono text-xs text-on-surface-variant">≤ 4.5%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Constraint Sensitivity Toggles */}
          <div className="bg-surface-container-lowest rounded-xl p-6 border border-outline-variant/40 shadow-sahara-soft">
            <h3 className="font-headline text-xl font-bold text-on-surface mb-5">Constraint Sensitivity</h3>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="font-body text-sm font-medium text-on-surface">Min Target Return</label>
                  <span className="font-mono text-xs text-primary font-semibold">{(store.minReturnConstraint * 100).toFixed(1)}%</span>
                </div>
                <input
                  type="range"
                  min="0.0"
                  max="0.15"
                  step="0.005"
                  value={store.minReturnConstraint}
                  onChange={(e) => store.setLppConstraints(parseFloat(e.target.value), store.maxConcentration)}
                  className="w-full h-1 bg-surface-variant rounded-full appearance-none outline-none"
                />
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="font-body text-sm font-medium text-on-surface">Max Single Asset Exposure</label>
                  <span className="font-mono text-xs text-on-surface-variant">{(store.maxConcentration * 100).toFixed(1)}%</span>
                </div>
                <input
                  type="range"
                  min="0.10"
                  max="1.00"
                  step="0.05"
                  value={store.maxConcentration}
                  onChange={(e) => store.setLppConstraints(store.minReturnConstraint, parseFloat(e.target.value))}
                  className="w-full h-1 bg-surface-variant rounded-full appearance-none outline-none"
                />
              </div>
              <div className="pt-2 flex justify-end">
                <button 
                  onClick={() => store.fetchOptimization()}
                  className="text-sm font-body font-semibold text-primary hover:text-primary-container transition-colors">
                  Recalculate Optimal Point
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Visuals & Output */}
        <div className="xl:col-span-7 flex flex-col gap-6 lg:gap-8">
          {/* The Simplex Path Optimizer */}
          <div className="bg-surface-container-lowest rounded-xl p-6 border border-outline-variant/40 shadow-sahara-soft h-80 relative flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-headline text-xl font-bold text-on-surface">Efficient Frontier Convergence</h3>
              <div className="flex gap-2">
                <span className="flex items-center gap-1 font-body text-xs text-on-surface-variant"><span className="w-2 h-2 rounded-full bg-secondary"></span> Current</span>
                <span className="flex items-center gap-1 font-body text-xs text-on-surface-variant"><span className="w-2 h-2 rounded-full bg-primary"></span> Optimal</span>
              </div>
            </div>
            {/* Abstract Representation of Chart (Data Visualization context) */}
            <div className="flex-1 w-full bg-surface-container-low rounded border border-outline-variant/20 relative overflow-hidden flex items-end px-4 pb-4">
              <div className="absolute left-4 bottom-4 top-4 w-px bg-outline-variant/60"></div>
              <div className="absolute left-4 bottom-4 right-4 h-px bg-outline-variant/60"></div>
              <span className="absolute left-6 top-4 font-body text-[10px] text-on-surface-variant tracking-wider">Expected Return</span>
              <span className="absolute right-4 bottom-6 font-body text-[10px] text-on-surface-variant tracking-wider">Risk (Volatility)</span>
              
              <div className="absolute left-4 bottom-4 w-[90%] h-[80%] border-l-0 border-b-0 border-t-2 border-r-2 border-primary/40 rounded-tr-[100%] opacity-50 transition-all duration-500"></div>
              <div className="absolute left-[40%] bottom-[30%] w-3 h-3 bg-secondary rounded-full shadow-md z-10 -translate-x-1/2 translate-y-1/2 ring-4 ring-secondary/20"></div>
              <svg className="absolute left-[40%] bottom-[30%] w-[20%] h-[30%] z-0" style={{ overflow: 'visible' }}>
                <line className="opacity-50" stroke="#c2652a" strokeDasharray="4 4" strokeWidth="1.5" x1="0" x2="100%" y1="0" y2="-100%"></line>
              </svg>
              <div className="absolute left-[60%] bottom-[60%] w-4 h-4 bg-primary rounded-full shadow-md z-10 -translate-x-1/2 translate-y-1/2 ring-4 ring-primary/30 flex items-center justify-center">
                <div className="w-1.5 h-1.5 bg-surface rounded-full"></div>
              </div>
              <div className="absolute left-[63%] bottom-[65%] bg-inverse-surface text-inverse-on-surface px-2 py-1 rounded text-[10px] font-body shadow-lg whitespace-nowrap">
                Sharpe Max Point
              </div>
            </div>
          </div>

          {/* Allocation Recommendations (Current vs Optimal Table) */}
          <div className="bg-surface-container-lowest rounded-xl p-0 border border-outline-variant/40 shadow-sahara-soft overflow-hidden flex-1">
            <div className="p-6 border-b border-outline-variant/30 flex justify-between items-center">
              <h3 className="font-headline text-xl font-bold text-on-surface">Capital Deployment Shift</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-container-low/50 font-body text-xs text-on-surface-variant uppercase tracking-wider">
                    <th className="px-6 py-4 font-semibold">Asset Class</th>
                    <th className="px-6 py-4 font-semibold text-right">Optimal Alloc.</th>
                    <th className="px-6 py-4 font-semibold text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="font-body text-sm divide-y divide-outline-variant/20">
                  {Object.entries(markowitz?.max_sharpe.weights || {}).map(([ticker, weight], idx) => {
                    const colors = ['#2a2420', '#78706a', '#c2652a', '#f0a878'];
                    return (
                      <tr key={ticker} className="hover:bg-surface-container-low/30 transition-colors">
                        <td className="px-6 py-4 font-medium text-on-surface flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: colors[idx % colors.length] }}></span> {ticker}
                        </td>
                        <td className="px-6 py-4 text-right font-semibold text-on-surface">{(weight * 100).toFixed(1)}%</td>
                        <td className="px-6 py-4 text-center">
                          {weight > 0 ? (
                            <span className="inline-flex items-center justify-center px-2 py-1 rounded bg-primary/10 text-primary text-xs font-bold border border-primary/20">BUY</span>
                          ) : (
                            <span className="inline-flex items-center justify-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant text-xs font-bold border border-outline-variant/40">HOLD</span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
