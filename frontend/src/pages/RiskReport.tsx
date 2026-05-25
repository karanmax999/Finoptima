import React from 'react';

export const RiskReport: React.FC = () => {
  return (
    <main className="flex-1 pt-4 pb-24 px-4 sm:px-8 max-w-[1600px] mx-auto w-full">
      {/* Header Section */}
      <div className="py-10 border-b border-outline-variant/40 mb-10">
        <h1 className="font-headline text-4xl sm:text-5xl font-bold text-on-surface tracking-tight mb-4 text-balance">Integrated Executive Risk Report</h1>
        <p className="font-body text-on-surface-variant text-lg max-w-3xl leading-relaxed">
          A comprehensive overview of portfolio health, predictive modeling outcomes, and regulatory compliance. The current optimization suggests a strategic shift towards defensive utility assets given recent macroeconomic volatility.
        </p>
      </div>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 lg:gap-8 mb-12">
        
        {/* Consolidated Risk Scorecard */}
        <section className="md:col-span-12 lg:col-span-8 bg-surface-container-lowest rounded-xl p-6 lg:p-8 shadow-sahara-soft border border-outline-variant/40">
          <h2 className="font-headline text-2xl font-bold text-on-surface mb-6 border-b border-outline-variant/40 pb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary">monitoring</span>
            Consolidated Risk Scorecard
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-4 bg-surface-container-low rounded-lg">
              <p className="font-body text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Total VaR (99%)</p>
              <p className="font-headline text-3xl font-bold text-on-surface mb-2">$4.2M</p>
              <p className="font-body text-xs text-error flex items-center gap-1 font-medium">
                <span className="material-symbols-outlined text-sm">trending_up</span> +0.8% vs last week
              </p>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg">
              <p className="font-body text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Diversification Score</p>
              <p className="font-headline text-3xl font-bold text-on-surface mb-2">84/100</p>
              <p className="font-body text-xs text-primary flex items-center gap-1 font-medium">
                <span className="material-symbols-outlined text-sm">trending_up</span> +2 pts vs last week
              </p>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg border border-primary/20 bg-primary/5">
              <p className="font-body text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Model Accuracy</p>
              <p className="font-headline text-3xl font-bold text-primary mb-2">0.92</p>
              <p className="font-body text-xs text-on-surface-variant flex items-center gap-1 font-medium">ROC-AUC</p>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg">
              <p className="font-body text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Expected Return</p>
              <p className="font-headline text-3xl font-bold text-on-surface mb-2">8.4%</p>
              <p className="font-body text-xs text-on-surface-variant flex items-center gap-1 font-medium">Annualized, Portfolio</p>
            </div>
          </div>

          {/* Abstract Chart representation */}
          <div className="mt-8 h-48 w-full bg-surface-container rounded-lg border border-outline-variant/30 flex items-end px-4 pt-8 pb-4 gap-2 relative overflow-hidden">
            <div className="absolute top-4 left-4 text-xs font-body text-on-surface-variant">Historical vs Predicted VaR Trajectory</div>
            <div className="w-full h-[60%] bg-surface-variant absolute bottom-0 left-0 opacity-50" style={{ clipPath: 'polygon(0 100%, 0 40%, 20% 60%, 40% 30%, 60% 50%, 80% 20%, 100% 40%, 100% 100%)' }}></div>
            <div className="w-full h-[80%] bg-primary-container/30 absolute bottom-0 left-0" style={{ clipPath: 'polygon(0 100%, 0 50%, 20% 70%, 40% 40%, 60% 60%, 80% 30%, 100% 10%, 100% 100%)', borderTop: '2px solid var(--color-primary)' }}></div>
            {/* Decorative bars */}
            <div className="flex-1 bg-outline-variant/40 rounded-t-sm h-[30%] z-10 hover:bg-primary/40 transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-outline-variant/40 rounded-t-sm h-[45%] z-10 hover:bg-primary/40 transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-outline-variant/40 rounded-t-sm h-[35%] z-10 hover:bg-primary/40 transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-outline-variant/40 rounded-t-sm h-[60%] z-10 hover:bg-primary/40 transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-primary/60 rounded-t-sm h-[75%] z-10 hover:bg-primary transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-primary/80 rounded-t-sm h-[50%] z-10 hover:bg-primary transition-colors cursor-pointer"></div>
            <div className="flex-1 bg-primary rounded-t-sm h-[85%] z-10 hover:opacity-80 transition-opacity cursor-pointer relative group">
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-inverse-surface text-inverse-on-surface text-xs py-1 px-2 rounded hidden group-hover:block whitespace-nowrap">Current Optimization</div>
            </div>
          </div>
        </section>

        {/* Regulatory Alignment Status */}
        <section className="md:col-span-12 lg:col-span-4 bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/40 flex flex-col">
          <h2 className="font-headline text-xl font-bold text-on-surface mb-6 border-b border-outline-variant/40 pb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-tertiary">gavel</span>
            Regulatory Alignment
          </h2>
          <div className="flex-1 space-y-4">
            <div className="flex items-start gap-4 p-4 rounded-lg bg-surface-container-low border border-outline-variant/20">
              <div className="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-primary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-primary text-sm font-bold">check</span>
              </div>
              <div>
                <h3 className="font-body font-bold text-on-surface mb-1">Basel III/IV Compliance</h3>
                <p className="font-body text-sm text-on-surface-variant">LCR and NSFR ratios comfortably exceed minimum regulatory thresholds.</p>
              </div>
            </div>
            <div className="flex items-start gap-4 p-4 rounded-lg bg-surface-container-low border border-outline-variant/20">
              <div className="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-primary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-primary text-sm font-bold">check</span>
              </div>
              <div>
                <h3 className="font-body font-bold text-on-surface mb-1">IFRS 9 ECL Modeling</h3>
                <p className="font-body text-sm text-on-surface-variant">Expected Credit Loss staging aligned with macro-economic stress scenarios.</p>
              </div>
            </div>
            <div className="flex items-start gap-4 p-4 rounded-lg bg-surface-variant/50 border border-outline-variant/40 border-dashed">
              <div className="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-surface-variant flex items-center justify-center">
                <span className="material-symbols-outlined text-on-surface-variant text-sm">schedule</span>
              </div>
              <div>
                <h3 className="font-body font-bold text-on-surface mb-1">FRTB Internal Models</h3>
                <p className="font-body text-sm text-on-surface-variant">Pending desk-level validation sign-off (Expected Q3).</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Module Breakdown Grid */}
      <h2 className="font-headline text-2xl font-bold text-on-surface mb-6 mt-12 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">view_quilt</span>
        Module Breakdown
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        
        {/* Market Risk */}
        <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/40">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-headline text-xl font-bold text-on-surface">Market Risk</h3>
            <span className="material-symbols-outlined text-outline">analytics</span>
          </div>
          <div className="mb-4">
            <p className="font-body text-sm text-on-surface-variant mb-2">Prior vs. Posterior Distribution Shift</p>
            {/* Abstract representation of distribution shift */}
            <div className="h-24 w-full relative mb-4">
              <svg className="w-full h-full text-surface-variant" preserveAspectRatio="none" viewBox="0 0 100 50">
                <path d="M0,50 Q25,50 50,20 T100,50" fill="none" stroke="currentColor" strokeWidth="2"></path>
              </svg>
              <svg className="w-full h-full text-primary absolute top-0 left-0" preserveAspectRatio="none" viewBox="0 0 100 50">
                <path d="M0,50 Q30,50 60,10 T100,50" fill="none" stroke="currentColor" strokeDasharray="4" strokeWidth="2"></path>
              </svg>
            </div>
          </div>
          <p className="font-body text-sm text-on-surface">Tail risk estimates have normalized post-adjustment, showing reduced sensitivity to interest rate shocks.</p>
        </div>

        {/* Systemic Vulnerability */}
        <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/40">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-headline text-xl font-bold text-on-surface">Systemic Vulnerability</h3>
            <span className="material-symbols-outlined text-outline">hub</span>
          </div>
          <div className="space-y-3 mb-4">
            <p className="font-body text-sm text-on-surface-variant mb-2">Highest Sector Correlations</p>
            <div className="flex items-center justify-between">
              <span className="font-body text-sm font-medium">Tech / Consumer Discretionary</span>
              <span className="font-body text-sm text-error font-bold">0.82</span>
            </div>
            <div className="w-full bg-surface-container rounded-full h-1.5">
              <div className="bg-error h-1.5 rounded-full" style={{ width: '82%' }}></div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="font-body text-sm font-medium">Energy / Materials</span>
              <span className="font-body text-sm text-primary font-bold">0.65</span>
            </div>
            <div className="w-full bg-surface-container rounded-full h-1.5">
              <div className="bg-primary h-1.5 rounded-full" style={{ width: '65%' }}></div>
            </div>
          </div>
          <p className="font-body text-sm text-on-surface pt-2 border-t border-outline-variant/20">Concentration risk identified in growth-oriented sectors.</p>
        </div>

        {/* Predictive Outlook */}
        <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/40">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-headline text-xl font-bold text-on-surface">Predictive Outlook</h3>
            <span className="material-symbols-outlined text-outline">query_stats</span>
          </div>
          <ul className="space-y-4 mb-4">
            <li className="flex gap-3 items-start">
              <span className="material-symbols-outlined text-primary text-sm mt-0.5">lightbulb</span>
              <p className="font-body text-sm text-on-surface"><strong className="block text-on-surface-variant font-medium">Alpha Generation:</strong> ML model identifies mispricing in mid-cap healthcare utilities.</p>
            </li>
            <li className="flex gap-3 items-start">
              <span className="material-symbols-outlined text-tertiary text-sm mt-0.5">warning</span>
              <p className="font-body text-sm text-on-surface"><strong className="block text-on-surface-variant font-medium">Default Prediction:</strong> Elevated probability of default detected in highly levered commercial real estate.</p>
            </li>
          </ul>
        </div>

        {/* Recommended Allocation (Full width below) */}
        <div className="md:col-span-2 lg:col-span-3 bg-surface-container-low rounded-xl p-6 shadow-sahara-soft border border-primary/20 flex flex-col md:flex-row gap-8 items-center">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="material-symbols-outlined text-primary">pie_chart</span>
              <h3 className="font-headline text-xl font-bold text-on-surface">Recommended Allocation</h3>
            </div>
            <p className="font-body text-sm text-on-surface-variant mb-4">Optimization engine suggests a definitive shift towards defensive asset classes.</p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm font-body">
                <span className="text-on-surface">Defensive Utilities</span>
                <span className="text-primary font-bold">+12%</span>
              </div>
              <div className="flex justify-between text-sm font-body">
                <span className="text-on-surface">High-Yield Bonds</span>
                <span className="text-error font-bold">-8%</span>
              </div>
              <div className="flex justify-between text-sm font-body">
                <span className="text-on-surface">Growth Equities</span>
                <span className="text-error font-bold">-4%</span>
              </div>
            </div>
          </div>
          <div className="flex-shrink-0 w-full md:w-auto flex flex-col sm:flex-row gap-4">
            <button className="bg-surface-container-lowest border border-outline-variant text-on-surface font-body font-medium px-6 py-3 rounded-lg hover:bg-surface-variant transition-colors flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-sm">download</span>
              Download Full Audit Log
            </button>
            <button className="bg-primary text-on-primary font-body font-bold px-8 py-3 rounded-lg shadow-sm hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-sm">check_circle</span>
              Approve Allocation
            </button>
          </div>
        </div>
      </div>
    </main>
  );
};
