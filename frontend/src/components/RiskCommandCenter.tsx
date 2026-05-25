import React, { useEffect, useState } from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { Shield, Brain, Scale } from 'lucide-react';

export const RiskCommandCenter: React.FC = () => {
  const store = useFinoptimaStore();
  
  // Local inputs before updating store to avoid lag
  const [income, setIncome] = useState(75000);
  const [score, setScore] = useState(720);
  const [term, setTerm] = useState(36);

  useEffect(() => {
    store.setBorrowerProfile(income, score, term);
  }, [income, score, term]);

  useEffect(() => {
    store.fetchBayesianScoring();
  }, [store.priorDefault, store.borrowerIncome, store.borrowerCreditScore, store.borrowerTerm]);

  const pDefault = store.bayesianResults?.posterior_probability ?? 0.0;
  const klImportance = store.bayesianResults?.feature_importance_kl ?? {};

  return (
    <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-6 rounded-2xl flex flex-col justify-between h-full">
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
            <Shield size={14} className="text-cyan-400" /> Risk Command Center
          </h3>
          <span className="text-slate-500 font-mono text-xxs flex items-center gap-1">
            <Brain size={12} className="text-indigo-400" /> Bayesian Scoring
          </span>
        </div>

        <div className="space-y-4">
          {/* Baseline slider prior */}
          <div>
            <div className="flex justify-between text-xxs font-mono text-slate-400 uppercase tracking-wider mb-1.5">
              <span>Baseline Default Prior:</span>
              <span className="text-cyan-400 font-bold">{(store.priorDefault * 100).toFixed(1)}%</span>
            </div>
            <input
              type="range"
              min="0.01"
              max="0.40"
              step="0.005"
              value={store.priorDefault}
              onChange={(e) => store.setPriorDefault(parseFloat(e.target.value))}
              className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
            />
          </div>

          {/* Interactive borrower profile metrics */}
          <div className="grid grid-cols-3 gap-3 bg-slate-950/40 p-3 rounded-lg border border-slate-850">
            <div>
              <label className="block text-slate-500 font-mono text-xxs mb-1">INCOME ($)</label>
              <input
                type="number"
                value={income}
                onChange={(e) => setIncome(Math.max(1000, parseInt(e.target.value) || 0))}
                className="w-full bg-slate-950 border border-slate-800 hover:border-slate-700/80 rounded px-2 py-1 text-xs font-mono text-cyan-300 transition-all outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-500 font-mono text-xxs mb-1">CREDIT SCORE</label>
              <input
                type="number"
                value={score}
                onChange={(e) => setScore(Math.min(850, Math.max(300, parseInt(e.target.value) || 0)))}
                className="w-full bg-slate-950 border border-slate-800 hover:border-slate-700/80 rounded px-2 py-1 text-xs font-mono text-cyan-300 transition-all outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-500 font-mono text-xxs mb-1">TERM (MO)</label>
              <input
                type="number"
                value={term}
                onChange={(e) => setTerm(Math.max(12, parseInt(e.target.value) || 0))}
                className="w-full bg-slate-950 border border-slate-800 hover:border-slate-700/80 rounded px-2 py-1 text-xs font-mono text-cyan-300 transition-all outline-none"
              />
            </div>
          </div>
        </div>

        {/* Bayesian calculations outputs */}
        <div className="mt-5 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-slate-500 font-mono text-xxs uppercase tracking-wider block">Posterior Probability P(Default | X)</span>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold font-display text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-amber-400">
                {(pDefault * 100).toFixed(2)}%
              </span>
              <span className="text-xxs font-mono text-slate-400">
                (Baseline: {(store.priorDefault * 100).toFixed(1)}%)
              </span>
            </div>
          </div>
          <div className="flex items-center gap-1 bg-slate-900 border border-slate-800/60 rounded-full px-2.5 py-1">
            <div className={`w-2 h-2 rounded-full ${pDefault > 0.15 ? 'bg-rose-500 animate-pulse' : 'bg-emerald-500'}`} />
            <span className="text-xxs font-mono text-slate-300 font-semibold">
              {pDefault > 0.25 ? 'High Risk' : pDefault > 0.10 ? 'Medium Risk' : 'Low Risk'}
            </span>
          </div>
        </div>
      </div>

      {/* Feature significance and weightings */}
      <div className="mt-4 border-t border-slate-800/80 pt-4">
        <span className="text-slate-500 font-mono text-xxs uppercase tracking-wider block mb-2 flex items-center gap-1">
          <Scale size={12} className="text-indigo-400" /> Feature Importance (KL Divergence)
        </span>
        <div className="space-y-2">
          {Object.entries(klImportance).map(([feature, val]) => (
            <div key={feature} className="space-y-1">
              <div className="flex justify-between text-xxs font-mono text-slate-400">
                <span>{feature}</span>
                <span className="text-indigo-300">{val.toFixed(4)}</span>
              </div>
              <div className="h-1 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-400 to-indigo-500 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(100, val * 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
export default RiskCommandCenter;
