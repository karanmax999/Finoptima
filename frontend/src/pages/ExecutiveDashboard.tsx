import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

export const ExecutiveDashboard: React.FC = () => {
  const store = useFinoptimaStore();
  
  // Use mock data from store if available
  const varParametric = store.apiResults?.risk_metrics.var_parametric_95 || 14200000;
  // Format as millions
  const varFormatted = (varParametric / 1000000).toFixed(1);

  return (
    <div className="p-8 pb-24 overflow-x-hidden">
      {/* Hero / Global Portfolio Health */}
      <div className="mb-10">
        <h1 className="font-headline text-4xl font-bold text-on-surface tracking-tight mb-2">Global Portfolio Health</h1>
        <p className="font-body text-on-surface-variant text-lg">Real-time consolidated view across all asset classes.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* VaR Metric Card (Hero) */}
        <div className="lg:col-span-2 bg-surface-container-lowest rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft flex flex-col justify-center relative overflow-hidden">
          <div className="absolute -right-20 -top-20 w-64 h-64 bg-primary-container/20 rounded-full blur-3xl"></div>
          <p className="font-body text-on-surface-variant font-medium text-sm tracking-wider uppercase mb-2 relative z-10">Value at Risk (VaR)</p>
          <div className="flex items-end gap-4 relative z-10 mb-4">
            <h2 className="font-headline text-6xl font-bold text-on-surface tracking-tighter">${varFormatted}M</h2>
            <span className="font-body text-primary font-semibold text-lg pb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-sm">trending_down</span> -2.4%
            </span>
          </div>
          <p className="font-body text-on-surface-variant/80 text-sm relative z-10 border-l-2 border-primary pl-3">At 99% confidence interval over a 10-day horizon.</p>
        </div>

        {/* Engine Status Card */}
        <div className="bg-surface-container-low rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft flex flex-col">
          <h3 className="font-headline text-xl font-bold text-on-surface mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary icon-fill">memory</span>
            Engine Status
          </h3>
          <div className="flex-1 flex flex-col justify-between gap-4">
            <div className="flex items-center justify-between">
              <span className="font-body text-sm text-on-surface-variant">Market Risk Module</span>
              <span className="flex items-center gap-1.5 font-body text-xs font-semibold text-primary"><span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>Active</span>
            </div>
            <div className="w-full bg-outline-variant/30 h-px"></div>
            <div className="flex items-center justify-between">
              <span className="font-body text-sm text-on-surface-variant">Credit Risk Engine</span>
              <span className="flex items-center gap-1.5 font-body text-xs font-semibold text-primary"><span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>Active</span>
            </div>
            <div className="w-full bg-outline-variant/30 h-px"></div>
            <div className="flex items-center justify-between">
              <span className="font-body text-sm text-on-surface-variant">Liquidity Analytics</span>
              <span className="flex items-center gap-1.5 font-body text-xs font-semibold text-primary"><span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>Active</span>
            </div>
            <div className="w-full bg-outline-variant/30 h-px"></div>
            <div className="flex items-center justify-between">
              <span className="font-body text-sm text-on-surface-variant">Stress Testing Framework</span>
              <span className="flex items-center gap-1.5 font-body text-xs font-semibold text-primary"><span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>Active</span>
            </div>
          </div>
        </div>
      </div>

      {/* Complex Bento Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        
        {/* Risk Heatmap (Spans 2 cols) */}
        <div className="md:col-span-2 bg-surface-container-lowest rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-headline text-xl font-bold text-on-surface">Risk Concentration</h3>
            <button className="text-primary hover:text-primary-container transition-colors text-sm font-semibold flex items-center gap-1">
              Expand <span className="material-symbols-outlined text-sm">open_in_new</span>
            </button>
          </div>
          {/* Abstract representation of a heatmap */}
          <div className="flex-1 rounded-lg overflow-hidden border border-outline-variant/40 flex flex-col min-h-[200px]">
            <div className="flex flex-1">
              <div className="w-1/3 bg-tertiary/80 p-3 flex flex-col justify-end text-on-primary transition-opacity hover:opacity-90 cursor-crosshair"><span className="text-xs font-semibold">Tech</span></div>
              <div className="w-1/4 bg-primary/40 p-3 flex flex-col justify-end text-on-surface transition-opacity hover:opacity-90 cursor-crosshair"><span className="text-xs font-semibold">Financials</span></div>
              <div className="flex-1 flex flex-col">
                <div className="h-1/2 bg-primary/20 p-3 flex flex-col justify-end text-on-surface transition-opacity hover:opacity-90 cursor-crosshair"><span className="text-xs font-semibold">Energy</span></div>
                <div className="h-1/2 flex">
                  <div className="w-1/2 bg-surface-variant p-2 flex flex-col justify-end text-on-surface-variant transition-opacity hover:opacity-90 cursor-crosshair"><span className="text-[10px] font-semibold">Healthcare</span></div>
                  <div className="w-1/2 bg-primary-container p-2 flex flex-col justify-end text-on-primary-container transition-opacity hover:opacity-90 cursor-crosshair"><span className="text-[10px] font-semibold">Real Estate</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bayesian Credit Score Summary */}
        <div className="md:col-span-2 bg-surface-container-lowest rounded-xl p-8 border border-outline-variant/60 shadow-sahara-soft flex flex-col">
          <h3 className="font-headline text-xl font-bold text-on-surface mb-6">Credit Quality Distribution</h3>
          <div className="flex-1 relative flex items-end justify-center pt-8 min-h-[200px]">
            {/* Abstract Bell Curve Representation using simple CSS geometry */}
            <div className="w-full h-full relative border-b border-outline-variant/60">
              <svg className="absolute bottom-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 50">
                <path d="M0,50 Q25,50 35,20 T50,5 T65,20 T100,50" fill="rgba(194, 101, 42, 0.15)" stroke="#c2652a" strokeWidth="2"></path>
              </svg>
              {/* Axis Labels */}
              <div className="absolute -bottom-6 w-full flex justify-between text-xs text-on-surface-variant font-body">
                <span>High Risk (CCC)</span>
                <span>Avg (BBB)</span>
                <span>Low Risk (AAA)</span>
              </div>
              {/* Median Marker */}
              <div className="absolute left-1/2 bottom-0 w-px h-full bg-outline border-dashed border-l z-10 flex flex-col items-center justify-start pt-2">
                <span className="bg-surface px-1 text-[10px] text-on-surface font-semibold rounded shadow-sm border border-outline-variant/40 relative -top-4">Current Mean</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Stress Test (Spans full width in this row) */}
        <div className="lg:col-span-4 bg-surface-container-low rounded-xl p-6 border border-outline-variant/60 shadow-sahara-soft flex flex-col md:flex-row items-center gap-8">
          <div className="w-16 h-16 rounded-full bg-surface-container-highest border border-outline-variant/80 flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-3xl text-tertiary">warning_amber</span>
          </div>
          <div className="flex-1">
            <p className="font-body text-xs font-semibold text-primary uppercase tracking-wider mb-1">Module 2 Result • 2 Hours Ago</p>
            <h4 className="font-headline text-lg font-bold text-on-surface mb-2">Severe Market Downturn Scenario</h4>
            <p className="font-body text-sm text-on-surface-variant">The latest simulation indicates a potential capital shortfall of <strong className="text-tertiary">$3.2M</strong> under a 30% aggregate market correction. Liquidity buffers remain sufficient.</p>
          </div>
          <div className="shrink-0 flex gap-3 w-full md:w-auto mt-4 md:mt-0">
            <button className="flex-1 md:flex-none px-4 py-2 bg-surface text-on-surface border border-outline-variant rounded-lg font-body text-sm font-semibold hover:bg-surface-variant transition-colors">View Details</button>
            <button className="flex-1 md:flex-none px-4 py-2 bg-primary text-on-primary rounded-lg font-body text-sm font-semibold hover:bg-primary/90 transition-colors">Mitigate</button>
          </div>
        </div>

      </div>
    </div>
  );
};
