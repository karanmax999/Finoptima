import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

export const PortfolioCorrelation: React.FC = () => {
  const store = useFinoptimaStore();
  const apiResults = store.apiResults;
  
  // Use real mock data if available
  const varParametric = apiResults?.risk_metrics.var_parametric_95 || 1420500;
  const varFormatted = (varParametric / 1000000).toFixed(1);

  return (
    <div className="p-8 lg:p-12 pb-24 overflow-x-hidden">
      {/* Header */}
      <div className="mb-10">
        <h1 className="font-headline text-4xl text-on-background mb-2">Portfolio Correlation Analysis</h1>
        <p className="text-on-surface-variant max-w-2xl text-lg">Evaluate cross-asset dependencies and systemic vulnerabilities under varied market conditions.</p>
      </div>

      {/* Metric Cards (Bento style row) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/30 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <span className="material-symbols-outlined text-6xl">scatter_plot</span>
          </div>
          <p className="text-sm font-medium text-on-surface-variant mb-1 uppercase tracking-wider">Diversification Score</p>
          <div className="flex items-end gap-3">
            <span className="font-headline text-4xl text-primary font-semibold">84.2</span>
            <span className="text-sm text-secondary mb-1">/ 100</span>
          </div>
          <p className="text-xs text-on-surface-variant mt-3 pt-3 border-t border-outline-variant/40">+2.1 from previous quarter</p>
        </div>
        
        <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sahara-soft border border-outline-variant/30">
          <p className="text-sm font-medium text-on-surface-variant mb-1 uppercase tracking-wider">Avg. Cross-Correlation</p>
          <div className="flex items-end gap-3">
            <span className="font-headline text-4xl text-on-background font-semibold">0.34</span>
          </div>
          <div className="mt-4 w-full bg-surface-container-highest rounded-full h-1.5">
            <div className="bg-secondary h-1.5 rounded-full" style={{ width: '34%' }}></div>
          </div>
          <p className="text-xs text-on-surface-variant mt-2 text-right">Moderate coupling</p>
        </div>
        
        <div className="bg-surface-container-low rounded-xl p-6 shadow-sahara-soft border border-primary/20">
          <div className="flex justify-between items-start">
            <p className="text-sm font-medium text-on-surface-variant mb-1 uppercase tracking-wider">Estimated VaR (99%)</p>
            <span className="material-symbols-outlined text-error text-sm">warning</span>
          </div>
          <div className="flex items-end gap-3">
            <span className="font-headline text-4xl text-tertiary font-semibold">${varFormatted}M</span>
          </div>
          <p className="text-xs text-on-surface-variant mt-3 pt-3 border-t border-outline-variant/40">10-day horizon projection</p>
        </div>
      </div>

      {/* Complex Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Asset Covariance Matrix (Takes up 2 columns on large screens) */}
        <div className="lg:col-span-2 bg-surface-container-lowest rounded-xl p-8 shadow-sahara-soft border border-outline-variant/30">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-headline text-2xl text-on-background">Asset Correlation Heatmap</h3>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 bg-surface-container rounded text-on-surface-variant">30D</span>
              <span className="px-2 py-1 bg-primary-container text-on-primary-container rounded font-medium">90D</span>
              <span className="px-2 py-1 bg-surface-container rounded text-on-surface-variant">1Y</span>
            </div>
          </div>
          <p className="text-sm text-on-surface-variant mb-6">Visualizing Pearson correlation coefficients across primary sectors.</p>
          
          {/* Heatmap Grid */}
          <div className="overflow-x-auto">
            <div className="min-w-[500px]">
              {/* Header Row */}
              <div className="flex mb-2">
                <div className="w-24"></div>
                <div className="flex-1 text-xs text-center font-medium text-on-surface-variant rotate-[-45deg] origin-bottom-left pb-2">Tech</div>
                <div className="flex-1 text-xs text-center font-medium text-on-surface-variant rotate-[-45deg] origin-bottom-left pb-2">Fin</div>
                <div className="flex-1 text-xs text-center font-medium text-on-surface-variant rotate-[-45deg] origin-bottom-left pb-2">Egy</div>
                <div className="flex-1 text-xs text-center font-medium text-on-surface-variant rotate-[-45deg] origin-bottom-left pb-2">RE</div>
                <div className="flex-1 text-xs text-center font-medium text-on-surface-variant rotate-[-45deg] origin-bottom-left pb-2">Hlth</div>
              </div>
              {/* Rows */}
              <div className="flex items-center mb-1">
                <div className="w-24 text-xs font-medium text-on-surface-variant">Technology</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-100 heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">1.0</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.6] heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">0.62</div>
                <div className="flex-1 aspect-square bg-[#8c3c3c] opacity-[0.2] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">-0.15</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.4] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.38</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.3] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.22</div>
              </div>
              <div className="flex items-center mb-1">
                <div className="w-24 text-xs font-medium text-on-surface-variant">Financials</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.6] heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">0.62</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-100 heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">1.0</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.5] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.45</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.7] heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">0.71</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.2] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.18</div>
              </div>
              <div className="flex items-center mb-1">
                <div className="w-24 text-xs font-medium text-on-surface-variant">Energy</div>
                <div className="flex-1 aspect-square bg-[#8c3c3c] opacity-[0.2] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">-0.15</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.5] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.45</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-100 heatmap-cell rounded-sm flex items-center justify-center text-white text-[10px]">1.0</div>
                <div className="flex-1 aspect-square bg-[#c2652a] opacity-[0.3] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">0.25</div>
                <div className="flex-1 aspect-square bg-[#8c3c3c] opacity-[0.1] heatmap-cell rounded-sm flex items-center justify-center text-[#3a302a] text-[10px]">-0.05</div>
              </div>
            </div>
          </div>
          
          {/* Legend */}
          <div className="flex items-center justify-end gap-4 mt-6 text-xs text-on-surface-variant">
            <span>Negative (-1.0)</span>
            <div className="w-32 h-2 rounded-full bg-gradient-to-r from-tertiary via-surface-variant to-primary opacity-80"></div>
            <span>Positive (1.0)</span>
          </div>
        </div>

        {/* VaR Calculator Column */}
        <div className="flex flex-col gap-8">
          {/* Value at Risk Card */}
          <div className="bg-surface-container-lowest rounded-xl p-8 shadow-sahara-soft border border-outline-variant/30 flex-1">
            <h3 className="font-headline text-2xl text-on-background mb-2">Value at Risk (VaR)</h3>
            <p className="text-sm text-on-surface-variant mb-6">Parametric estimation mapping potential tail loss.</p>
            
            {/* Distribution Visualization */}
            <div className="distribution-curve rounded-t-lg mb-4 relative">
              <svg className="curve-path" preserveAspectRatio="none" viewBox="0 0 100 100">
                <path d="M0,100 C20,90 30,10 50,10 C70,10 80,90 100,100"></path>
              </svg>
              {/* VaR Line Marker */}
              <div className="absolute top-0 bottom-0 left-[15%] w-px bg-tertiary border-l border-dashed border-tertiary"></div>
              <div className="absolute bottom-2 left-[5%] text-[10px] text-tertiary font-bold">Tail Risk</div>
            </div>
            
            <div className="flex justify-between text-xs text-on-surface-variant border-b border-outline-variant/40 pb-4 mb-4">
              <div>
                <p className="mb-1">Confidence Interval</p>
                <div className="flex gap-2">
                  <button className="px-2 py-1 bg-surface-container rounded hover:bg-surface-variant transition">95%</button>
                  <button className="px-2 py-1 bg-primary-container text-on-primary-container rounded font-medium">99%</button>
                </div>
              </div>
              <div className="text-right">
                <p className="mb-1">Time Horizon</p>
                <span className="font-medium text-on-background">10 Days</span>
              </div>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Estimated Loss</span>
              <span className="font-headline text-xl text-tertiary font-semibold">-${varParametric.toLocaleString()}</span>
            </div>
          </div>

          {/* Stress Testing Simulator (CLT) mini-view */}
          <div className="bg-surface-container rounded-xl p-6 shadow-sahara-soft border border-outline-variant/30 relative group overflow-hidden">
            {/* Decorative bg */}
            <div className="absolute -right-8 -top-8 w-32 h-32 bg-primary/5 rounded-full blur-2xl"></div>
            
            <h4 className="font-headline text-lg text-on-background mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-sm">science</span>
              CLT Stress Simulator
            </h4>
            
            {/* Mini Bar Chart simulating CLT shifting */}
            <div className="flex items-end h-24 gap-1 mb-4 border-b border-outline-variant/50 pb-1">
              <div className="w-full bg-surface-variant rounded-t-sm h-[20%] clt-bar group-hover:bg-tertiary/20 group-hover:h-[40%]"></div>
              <div className="w-full bg-surface-variant rounded-t-sm h-[40%] clt-bar group-hover:bg-tertiary/40 group-hover:h-[60%]"></div>
              <div className="w-full bg-outline-variant rounded-t-sm h-[80%] clt-bar group-hover:bg-tertiary/60 group-hover:h-[70%]"></div>
              <div className="w-full bg-primary/40 rounded-t-sm h-[100%] clt-bar group-hover:bg-tertiary/80 group-hover:h-[40%]"></div>
              <div className="w-full bg-outline-variant rounded-t-sm h-[80%] clt-bar group-hover:bg-primary/40 group-hover:h-[20%]"></div>
              <div className="w-full bg-surface-variant rounded-t-sm h-[40%] clt-bar group-hover:bg-surface-variant group-hover:h-[10%]"></div>
              <div className="w-full bg-surface-variant rounded-t-sm h-[20%] clt-bar group-hover:bg-surface-variant group-hover:h-[5%]"></div>
            </div>
            
            <p className="text-xs text-on-surface-variant mb-4">Simulates distribution shift under a '2008 Financial Crisis' scenario.</p>
            <button className="w-full py-2 border border-primary text-primary rounded-lg text-sm font-medium hover:bg-primary/5 transition-colors">Configure Scenario</button>
          </div>
        </div>
      </div>
    </div>
  );
};
