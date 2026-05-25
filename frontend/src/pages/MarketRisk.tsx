import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

export const MarketRisk: React.FC = () => {
  const store = useFinoptimaStore();
  const bayesian = store.bayesianResults;
  
  const klShift = bayesian ? (bayesian.posterior_probability - bayesian.prior_baseline) * 100 : 4.2;
  const isIncrease = klShift > 0;

  return (
    <div className="p-6 md:p-10">
      {/* Hero/Header Section */}
      <div className="max-w-3xl mb-12">
        <p className="text-tertiary font-bold tracking-widest uppercase text-xs mb-3">Default Probability Engine</p>
        <h1 className="text-5xl md:text-6xl text-on-surface font-headline leading-tight mb-6">
          Demystifying the <br /><i className="text-primary font-normal">Black Box</i>.
        </h1>
        <p className="text-lg text-on-surface-variant font-body leading-relaxed max-w-2xl">
          Statistical transparency through interactive probabilistic modeling. Observe market dynamics shift from historical priors to real-time posteriors.
        </p>
      </div>

      {/* Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Bayesian Credit Scoring Workbench (Span 8) */}
        <div className="md:col-span-8 bg-surface-container-lowest rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft relative overflow-hidden group">
          <div className="flex justify-between items-start mb-8 z-10 relative">
            <div>
              <h3 className="font-headline text-2xl text-on-surface mb-1">Bayesian Credit Scoring</h3>
              <p className="text-sm text-on-surface-variant font-body">Prior vs. Posterior Distribution Dynamics</p>
            </div>
            <div className="flex items-center gap-2 bg-surface-container rounded-full px-3 py-1 border border-outline-variant/40">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
              <span className="text-xs font-medium text-on-surface-variant uppercase tracking-wider">Live Model</span>
            </div>
          </div>

          {/* Abstract Visualization Area */}
          <div className="h-64 w-full relative flex items-end mb-4 border-b border-outline-variant/40 pb-4">
            {/* Prior Curve (Subtle) */}
            <svg className="absolute bottom-4 left-0 w-full h-full opacity-30 text-secondary" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path d="M0,100 C20,100 30,20 50,20 C70,20 80,100 100,100" fill="none" stroke="currentColor" strokeWidth="2" vectorEffect="non-scaling-stroke"></path>
              <path d="M0,100 C20,100 30,20 50,20 C70,20 80,100 100,100 L100,100 L0,100 Z" fill="currentColor" opacity="0.1"></path>
            </svg>
            
            {/* Posterior Curve (Prominent Sienna) */}
            <svg className="absolute bottom-4 left-10 w-[90%] h-[110%] text-primary transition-transform duration-1000 ease-in-out group-hover:scale-105" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path d="M0,100 C25,100 40,5 55,5 C70,5 85,100 100,100" fill="none" stroke="currentColor" strokeWidth="3" vectorEffect="non-scaling-stroke"></path>
              <path d="M0,100 C25,100 40,5 55,5 C70,5 85,100 100,100 L100,100 L0,100 Z" fill="url(#sienna-grad)" opacity="0.15"></path>
              <defs>
                <linearGradient id="sienna-grad" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="currentColor"></stop>
                  <stop offset="100%" stopColor="transparent"></stop>
                </linearGradient>
              </defs>
            </svg>
            
            <div className="absolute bottom-0 w-full flex justify-between text-[10px] text-on-surface-variant uppercase tracking-widest font-medium">
              <span>Lower Risk</span>
              <span>Default Probability</span>
              <span>Higher Risk</span>
            </div>
          </div>
        </div>

        {/* Confidence Update (Span 4) */}
        <div className="md:col-span-4 bg-surface-container rounded-xl p-8 border border-outline-variant/40 shadow-sahara-soft flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-tertiary">
              <span className="material-symbols-outlined text-lg">radar</span>
              <span className="text-xs font-bold tracking-widest uppercase">Confidence Update</span>
            </div>
            <p className="text-sm text-on-surface-variant mt-2 leading-relaxed">
              Information gain from recent macroeconomic indicators incorporated into the posterior estimate.
            </p>
          </div>
          <div className="mt-8">
            <div className="font-headline text-6xl text-primary tracking-tighter mb-1">
              {isIncrease ? '+' : ''}{klShift.toFixed(1)}<span className="text-3xl text-on-surface-variant ml-1">%</span>
            </div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider font-medium border-t border-outline-variant/60 pt-3 mt-4">
              Divergence (KL) Shift
            </div>
          </div>
        </div>

        {/* Asset Return Distributions (Span 6) */}
        <div className="md:col-span-6 bg-surface-container-lowest rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-headline text-xl text-on-surface">Asset Return Distributions</h3>
            <span className="material-symbols-outlined text-outline">stacked_line_chart</span>
          </div>
          
          <div className="flex h-40 items-end gap-1 mb-2">
            {[10, 25, 45, 85, 100, 70, 40, 20, 10, 5].map((height, i) => (
              <div key={i} className={`w-full ${height >= 85 ? (height === 100 ? 'bg-primary opacity-90' : 'bg-primary-container') : 'bg-surface-variant'} rounded-t-sm relative group`} style={{ height: `${height}%` }}>
                <div className="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                {height === 100 && (
                  <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-inverse-surface text-inverse-on-surface text-xs px-2 py-1 rounded hidden group-hover:block whitespace-nowrap z-10">Peak Prob.</div>
                )}
              </div>
            ))}
          </div>
          <p className="text-xs text-on-surface-variant text-center mt-4 italic">Lognormal probability density function</p>
        </div>

        {/* Operational Risk Monitor (Span 6) */}
        <div className="md:col-span-6 bg-surface-container-low rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-headline text-xl text-on-surface">Operational Risk Monitor</h3>
            <span className="material-symbols-outlined text-outline">warning</span>
          </div>
          <div className="flex items-center gap-6 h-40">
            <div className="flex-1">
              <div className="text-4xl font-headline text-tertiary mb-1">λ = 0.04</div>
              <p className="text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-4">Poisson Rate Parameter</p>
              <p className="text-sm text-on-surface-variant leading-relaxed">Modeling probabilities of rare anomalous events (e.g., fraud execution vectors) across transactional strata.</p>
            </div>
            <div className="w-32 h-32 rounded-full border-4 border-surface-variant border-t-tertiary border-r-tertiary transform rotate-45 relative">
              <div className="absolute inset-0 flex items-center justify-center -rotate-45">
                <span className="text-xl font-headline text-on-surface">P(k&gt;0)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Data Ingestion Status (Span 12) */}
        <div className="md:col-span-12 bg-surface-container-lowest rounded-xl border border-outline-variant/60 overflow-hidden mt-4 shadow-sahara-soft">
          <div className="bg-surface-container px-6 py-3 border-b border-outline-variant/40 flex justify-between items-center">
            <h4 className="text-sm font-bold uppercase tracking-wider text-on-surface">Data Ingestion Status</h4>
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
          </div>
          <div className="p-0 max-h-48 overflow-y-auto">
            <table className="w-full text-left text-sm font-body">
              <tbody>
                <tr className="border-b border-outline-variant/20 hover:bg-surface-variant/30 transition-colors">
                  <td className="py-3 px-6 text-on-surface-variant font-mono text-xs">14:02:45 GMT</td>
                  <td className="py-3 px-6 text-on-surface font-medium">Bloomberg BVAL Feed</td>
                  <td className="py-3 px-6 text-on-surface-variant">Parsed 45k instruments</td>
                  <td className="py-3 px-6 text-right"><span className="text-primary text-xs font-bold uppercase tracking-wider">Success</span></td>
                </tr>
                <tr className="border-b border-outline-variant/20 hover:bg-surface-variant/30 transition-colors">
                  <td className="py-3 px-6 text-on-surface-variant font-mono text-xs">14:02:42 GMT</td>
                  <td className="py-3 px-6 text-on-surface font-medium">Macro Indicators API</td>
                  <td className="py-3 px-6 text-on-surface-variant">Yield curve update applied</td>
                  <td className="py-3 px-6 text-right"><span className="text-primary text-xs font-bold uppercase tracking-wider">Success</span></td>
                </tr>
                <tr className="hover:bg-surface-container-low/30 transition-colors">
                  <td className="py-3 px-6 text-on-surface-variant font-mono text-xs">14:02:10 GMT</td>
                  <td className="py-3 px-6 text-on-surface font-medium">Internal Ledger Sync</td>
                  <td className="py-3 px-6 text-on-surface-variant">Reconciling tier 1 capital</td>
                  <td className="py-3 px-6 text-right"><span className="text-outline text-xs font-bold uppercase tracking-wider">Processing</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
