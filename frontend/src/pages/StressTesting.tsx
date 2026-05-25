import React, { useState, useEffect } from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

// Stress multipliers applied to baseline VaR/CVaR
function applyStress(baseVar: number, equityCrash: number, volSurge: number, rateBps: number): number {
  const equityFactor = 1 + equityCrash / 100;
  const volFactor = 1 + (volSurge - 20) / 100;
  const rateFactor = 1 + rateBps / 10000;
  return baseVar * equityFactor * volFactor * rateFactor;
}

const PRESETS: Record<string, { rate: number; equity: number; vix: number; spread: number }> = {
  'Custom Configuration':    { rate: 0,   equity: 0,  vix: 20,  spread: 0   },
  '2008 Financial Crisis':   { rate: 50,  equity: 55, vix: 80,  spread: 600 },
  '1987 Black Monday':       { rate: 100, equity: 22, vix: 60,  spread: 300 },
  'COVID-19 Market Shock':   { rate: 0,   equity: 34, vix: 85,  spread: 400 },
  'Dot-Com Bubble Burst':    { rate: 200, equity: 49, vix: 45,  spread: 250 },
};

export const StressTesting: React.FC = () => {
  const { apiResults, isCalculating, fetchOptimization } = useFinoptimaStore();

  const [preset, setPreset]   = useState('Custom Configuration');
  const [rate, setRate]       = useState(250);
  const [equity, setEquity]   = useState(45);
  const [vix, setVix]         = useState(85);
  const [spread, setSpread]   = useState(400);
  const [applied, setApplied] = useState(false);

  // Load preset values
  useEffect(() => {
    const p = PRESETS[preset];
    if (p) { setRate(p.rate); setEquity(p.equity); setVix(p.vix); setSpread(p.spread); }
  }, [preset]);

  // Fetch baseline data on mount if not already loaded
  useEffect(() => {
    if (!apiResults) fetchOptimization();
  }, []);

  const handleApply = async () => {
    await fetchOptimization();
    setApplied(true);
  };

  // Derive stressed metrics from live API data
  const baseVar   = apiResults?.risk_metrics?.var_historical_95  ?? 0;
  const baseCvar  = apiResults?.risk_metrics?.cvar_historical_95 ?? 0;
  const stressedVar  = applied ? applyStress(Math.abs(baseVar),  equity, vix, rate) : Math.abs(baseVar);
  const stressedCvar = applied ? applyStress(Math.abs(baseCvar), equity, vix, rate) : Math.abs(baseCvar);

  // CET1 proxy: stressed capital ratio
  const baselineCet1  = 12.4;
  const stressedCet1  = applied ? Math.max(0, baselineCet1 - (equity / 100) * 8 - (rate / 500) * 2).toFixed(1) : baselineCet1.toFixed(1);
  const cet1Pct       = (parseFloat(stressedCet1) / 20) * 100;

  // LCR proxy
  const baseLcr      = 125;
  const stressedLcr  = applied ? Math.max(0, baseLcr - (equity / 100) * 50 - (vix / 120) * 20).toFixed(0) : baseLcr.toFixed(0);
  const daysToDeplete = applied ? Math.max(1, Math.round(30 * (parseFloat(stressedLcr) / 100))).toString() : '30+';

  void apiResults?.markowitz?.frontier; // available for future chart extensions

  return (
    <div className="flex-1 p-10 flex flex-col gap-10">
      {/* Header */}
      <header className="flex justify-between items-end">
        <div className="max-w-2xl">
          <h1 className="font-headline text-4xl text-on-surface mb-3 tracking-tight">Global Stress Testing Simulator</h1>
          <p className="text-lg text-on-surface-variant font-body">Configure extreme market scenarios to evaluate portfolio resilience and simulate potential capital depletion events.</p>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={() => { setPreset('Custom Configuration'); setApplied(false); fetchOptimization(); }}
            className="px-5 py-2.5 rounded-lg border border-outline-variant text-on-surface font-semibold hover:bg-surface-container transition-colors text-sm"
          >
            Reset Baseline
          </button>
          <button className="px-5 py-2.5 rounded-lg border border-outline-variant text-on-surface font-semibold hover:bg-surface-container transition-colors text-sm flex items-center gap-2">
            <span className="material-symbols-outlined text-[18px]">description</span> Regulatory Report
          </button>
          <button
            onClick={handleApply}
            disabled={isCalculating}
            className="px-6 py-2.5 rounded-lg bg-primary text-on-primary font-semibold hover:bg-primary/90 transition-colors text-sm shadow-sm disabled:opacity-50"
          >
            {isCalculating ? 'Calculating…' : 'Apply Scenario'}
          </button>
        </div>
      </header>

      {/* Bento Grid */}
      <div className="grid grid-cols-12 gap-8">

        {/* Left: Scenario Config */}
        <div className="col-span-12 xl:col-span-4 sahara-card p-8 flex flex-col gap-8">
          <div>
            <h3 className="font-headline text-2xl text-on-surface mb-1">Scenario Parameters</h3>
            <p className="text-sm text-on-surface-variant">Adjust macro stressors or load historical configurations.</p>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-secondary mb-2">Historical Preset</label>
            <div className="relative">
              <select
                value={preset}
                onChange={e => setPreset(e.target.value)}
                className="w-full bg-surface-container border border-outline-variant rounded-lg py-3 px-4 appearance-none focus:ring-1 focus:ring-primary focus:border-primary text-on-surface font-body"
              >
                {Object.keys(PRESETS).map(k => <option key={k}>{k}</option>)}
              </select>
              <span className="material-symbols-outlined absolute right-4 top-3.5 text-on-surface-variant pointer-events-none">expand_more</span>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-semibold text-on-surface">Interest Rate Spike</label>
                <span className="text-sm font-bold text-primary">+{rate} bps</span>
              </div>
              <input type="range" min="0" max="500" value={rate} onChange={e => setRate(+e.target.value)}
                className="w-full h-1 bg-surface-variant rounded-lg appearance-none cursor-pointer accent-primary" />
            </div>
            <div>
              <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-semibold text-on-surface">Equity Market Crash</label>
                <span className="text-sm font-bold text-primary">-{equity}%</span>
              </div>
              <input type="range" min="0" max="80" value={equity} onChange={e => setEquity(+e.target.value)}
                className="w-full h-1 bg-surface-variant rounded-lg appearance-none cursor-pointer accent-primary" />
            </div>
            <div>
              <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-semibold text-on-surface">Volatility Surge (VIX)</label>
                <span className="text-sm font-bold text-primary">{vix}</span>
              </div>
              <input type="range" min="15" max="120" value={vix} onChange={e => setVix(+e.target.value)}
                className="w-full h-1 bg-surface-variant rounded-lg appearance-none cursor-pointer accent-primary" />
            </div>
            <div>
              <div className="flex justify-between items-end mb-2">
                <label className="text-sm font-semibold text-on-surface">Credit Spread Widening</label>
                <span className="text-sm font-bold text-primary">+{spread} bps</span>
              </div>
              <input type="range" min="0" max="800" value={spread} onChange={e => setSpread(+e.target.value)}
                className="w-full h-1 bg-surface-variant rounded-lg appearance-none cursor-pointer accent-primary" />
            </div>
          </div>

          {/* Live VaR summary */}
          {apiResults && (
            <div className="mt-2 p-4 bg-surface-container rounded-lg border border-outline-variant/50 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Baseline 95% VaR</span>
                <span className="font-bold text-on-surface">${Math.abs(baseVar).toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Stressed VaR</span>
                <span className="font-bold text-tertiary">${stressedVar.toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Stressed CVaR</span>
                <span className="font-bold text-tertiary">${stressedCvar.toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
              </div>
            </div>
          )}

          <div className="mt-auto pt-4 border-t border-outline-variant/50">
            <div className="flex items-center gap-3 text-sm text-on-surface-variant">
              <span className="material-symbols-outlined text-secondary">info</span>
              <p>Model confidence interval set to 99.9% VaR.</p>
            </div>
          </div>
        </div>

        {/* Right: Visualizations */}
        <div className="col-span-12 xl:col-span-8 flex flex-col gap-8">

          {/* Density Impact Chart */}
          <div className="sahara-card p-8 flex-1 min-h-[400px] flex flex-col">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="font-headline text-2xl text-on-surface mb-1">Probability Density Impact</h3>
                <p className="text-sm text-on-surface-variant">Portfolio Value Distribution (Baseline vs. Stressed)</p>
              </div>
              <div className="flex gap-4 text-sm font-medium">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 border-t-2 border-dashed border-outline"></div>
                  <span className="text-secondary">Baseline</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-primary/20 border border-primary rounded-sm"></div>
                  <span className="text-primary">Stressed</span>
                </div>
              </div>
            </div>

            <div className="flex-1 relative w-full h-full mt-4 flex items-end">
              <svg className="w-full h-[280px]" preserveAspectRatio="none" viewBox="0 0 800 300">
                <line opacity="0.5" stroke="#d8d0c8" strokeDasharray="2" strokeWidth="1" x1="0" y1="50"  x2="800" y2="50"/>
                <line opacity="0.5" stroke="#d8d0c8" strokeDasharray="2" strokeWidth="1" x1="0" y1="150" x2="800" y2="150"/>
                <line opacity="0.5" stroke="#d8d0c8" strokeDasharray="2" strokeWidth="1" x1="0" y1="250" x2="800" y2="250"/>

                {/* Baseline curve */}
                <path className="chart-curve-base" d="M 50,280 Q 200,280 350,150 T 600,280"/>

                {/* Stressed curve — shifts left proportional to equity crash */}
                {applied && (
                  <path className="chart-curve-stress"
                    d={`M ${Math.max(5, 20 - equity / 4)},280 Q ${Math.max(80, 150 - equity)},280 ${Math.max(150, 250 - equity * 1.5)},${Math.max(40, 80 - vix / 4)} T ${Math.max(350, 500 - equity * 2)},280 Z`}
                  />
                )}
                {!applied && (
                  <path className="chart-curve-stress" d="M 20,280 Q 150,280 250,80 T 500,280 Z"/>
                )}

                {/* VaR markers */}
                <line stroke="#8c3c3c" strokeDasharray="4" strokeWidth="1"
                  x1={applied ? Math.max(80, 180 - equity * 2) : 180}
                  y1="80"
                  x2={applied ? Math.max(80, 180 - equity * 2) : 180}
                  y2="280"/>
                <text fill="#8c3c3c" fontFamily="Manrope" fontSize="12"
                  x={applied ? Math.max(85, 185 - equity * 2) : 185} y="100">
                  Stressed 99% VaR
                </text>

                <line stroke="#78706a" strokeDasharray="4" strokeWidth="1" x1="280" y1="150" x2="280" y2="280"/>
                <text fill="#78706a" fontFamily="Manrope" fontSize="12" x="285" y="165">Current 99% VaR</text>

                <line stroke="#9a9088" strokeWidth="2" x1="0" y1="280" x2="800" y2="280"/>
              </svg>

              <div className="absolute bottom-[-24px] w-full flex justify-between text-xs text-secondary font-medium px-4">
                <span>-$500M</span><span>-$250M</span><span>$0</span><span>+$250M</span><span>+$500M</span>
              </div>
            </div>
          </div>

          {/* Metrics Row */}
          <div className="grid grid-cols-2 gap-8">
            {/* CET1 */}
            <div className="sahara-card p-6 flex flex-col justify-between">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h4 className="font-headline text-xl text-on-surface">CET1 Capital Adequacy</h4>
                  <span className="text-xs text-on-surface-variant uppercase tracking-wider font-bold">Tier 1 Ratio</span>
                </div>
                <span className="material-symbols-outlined text-tertiary p-2 bg-error-container rounded-full">warning</span>
              </div>
              <div className="flex items-end gap-4 mb-4">
                <span className="text-5xl font-headline text-tertiary tracking-tight">{stressedCet1}%</span>
                <span className="text-sm text-secondary mb-1 line-through">{baselineCet1}% Baseline</span>
              </div>
              <div className="w-full relative">
                <div className="w-full h-2 bg-surface-variant rounded-full overflow-hidden">
                  <div className="h-full bg-tertiary rounded-full transition-all duration-500" style={{ width: `${Math.min(100, cet1Pct)}%` }}></div>
                </div>
                <div className="absolute top-[-4px] bottom-[-4px] w-0.5 bg-on-surface left-[30%]" title="Basel III Minimum (4.5%)"></div>
                <span className="absolute top-4 left-[28%] text-[10px] text-secondary font-bold">BASEL III MIN</span>
              </div>
              <p className="text-sm text-tertiary font-medium mt-6 bg-tertiary-fixed/30 p-3 rounded-lg border border-tertiary-fixed-dim">
                {parseFloat(stressedCet1) < 4.5
                  ? 'Scenario breaches Basel III minimum capital requirements.'
                  : 'Scenario triggers severe capital depletion approaching regulatory minimums.'}
              </p>
            </div>

            {/* LCR */}
            <div className="sahara-card p-6 flex flex-col justify-between">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h4 className="font-headline text-xl text-on-surface">Liquidity Coverage (LCR)</h4>
                  <span className="text-xs text-on-surface-variant uppercase tracking-wider font-bold">30-Day Stress</span>
                </div>
                <span className="material-symbols-outlined text-primary p-2 bg-surface-container rounded-full">water_drop</span>
              </div>
              <div className="flex items-end gap-4 mb-4">
                <span className="text-5xl font-headline text-primary tracking-tight">{stressedLcr}%</span>
                <span className="text-sm text-secondary mb-1">vs {baseLcr}% Baseline</span>
              </div>
              <div className="h-12 w-full mt-2 relative overflow-hidden">
                <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 40">
                  <path d={`M 0,10 Q 20,15 40,${applied ? 25 + equity / 5 : 20} T 100,${applied ? 35 + equity / 10 : 25}`}
                    fill="none" stroke="#c2652a" strokeWidth="2"/>
                  <circle cx="100" cy={applied ? 35 + equity / 10 : 25} fill="#c2652a" r="3"/>
                </svg>
              </div>
              <div className="flex items-center gap-2 mt-4 text-sm text-on-surface-variant border-t border-outline-variant/40 pt-4">
                <span className="material-symbols-outlined text-[16px]">hourglass_empty</span>
                Time to Depletion: <strong className="text-on-surface">{daysToDeplete} Days</strong>
              </div>
            </div>
          </div>

          {/* Live tickers from API */}
          {apiResults && (
            <div className="sahara-card p-6">
              <h4 className="font-headline text-lg text-on-surface mb-4">Live Portfolio — Stressed Exposure</h4>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                {apiResults.tickers.map((ticker, i) => {
                  const ret = apiResults.expected_returns[i];
                  const vol = apiResults.volatilities[i];
                  const stressedVol = applied ? vol * (1 + equity / 100) * (1 + (vix - 20) / 100) : vol;
                  return (
                    <div key={ticker} className="bg-surface-container rounded-lg p-3 text-center">
                      <div className="font-bold text-on-surface text-sm">{ticker}</div>
                      <div className={`text-xs mt-1 ${ret >= 0 ? 'text-primary' : 'text-tertiary'}`}>
                        μ {(ret * 100).toFixed(3)}%
                      </div>
                      <div className="text-xs text-on-surface-variant">
                        σ {(stressedVol * 100).toFixed(2)}%{applied ? ' ⚠' : ''}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
