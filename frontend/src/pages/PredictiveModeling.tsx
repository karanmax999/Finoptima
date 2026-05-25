import React from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';

export const PredictiveModeling: React.FC = () => {
  const store = useFinoptimaStore();
  const regResults = store.apiResults?.regression_diagnostics;
  
  // Use mock data from store if available
  const rSquared = regResults ? regResults.r_squared : 0.684;
  const adjRSquared = regResults ? regResults.adjusted_r_squared : 0.679;

  return (
    <main className="flex-1 p-8 lg:p-12 max-w-7xl mx-auto overflow-x-hidden">
      {/* Header Section */}
      <div className="mb-12">
        <h1 className="text-4xl lg:text-5xl font-headline font-semibold text-on-surface tracking-tight mb-3">Predictive Modeling Workbench</h1>
        <p className="text-lg text-on-surface-variant font-body max-w-2xl">Interpretable alpha generation and default prediction models.</p>
      </div>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Logistic Regression (Default Prediction) - Large Panel */}
        <div className="lg:col-span-8 bg-surface-container-low rounded-2xl p-8 border border-outline-variant/60 shadow-sahara-soft">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-2xl font-headline font-semibold text-on-surface mb-1 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">trending_down</span>
                Logistic Regression: Default Prediction
              </h2>
              <p className="text-sm text-on-surface-variant">Retail Credit Portfolio (N=14,205)</p>
            </div>
            <div className="px-3 py-1 bg-surface-variant rounded-full text-xs font-semibold text-on-surface-variant border border-outline-variant/50">
              Status: Active Model
            </div>
          </div>

          {/* Placeholder for Sigmoid Chart */}
          <div className="w-full h-64 bg-surface-bright rounded-xl border border-outline-variant/40 mb-8 relative overflow-hidden flex items-center justify-center">
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-surface-variant/30 to-transparent"></div>
            {/* Abstract representation of a sigmoid */}
            <svg className="w-full h-full opacity-60" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path className="text-primary" d="M 0 90 C 40 90, 60 10, 100 10" fill="none" stroke="currentColor" strokeWidth="2"></path>
              <line className="text-outline-variant" stroke="currentColor" strokeDasharray="2 2" strokeWidth="0.5" x1="50" x2="50" y1="0" y2="100"></line>
              <line className="text-outline-variant" stroke="currentColor" strokeDasharray="2 2" strokeWidth="0.5" x1="0" x2="100" y1="50" y2="50"></line>
            </svg>
            <span className="absolute bottom-4 right-4 text-xs text-on-surface-variant bg-surface-bright/80 px-2 py-1 rounded backdrop-blur-sm border border-outline-variant/40">Probability of Default P(Y=1)</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Metrics */}
            <div>
              <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider mb-4 border-b border-outline-variant/40 pb-2">Model Performance</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-surface-bright p-4 rounded-lg border border-outline-variant/30">
                  <p className="text-xs text-on-surface-variant mb-1">Accuracy</p>
                  <p className="text-xl font-headline font-semibold text-on-surface">92.4%</p>
                </div>
                <div className="bg-surface-bright p-4 rounded-lg border border-outline-variant/30">
                  <p className="text-xs text-on-surface-variant mb-1">Precision</p>
                  <p className="text-xl font-headline font-semibold text-on-surface">88.7%</p>
                </div>
                <div className="bg-surface-bright p-4 rounded-lg border border-outline-variant/30">
                  <p className="text-xs text-on-surface-variant mb-1">Recall</p>
                  <p className="text-xl font-headline font-semibold text-on-surface">85.2%</p>
                </div>
                <div className="bg-primary-container/20 p-4 rounded-lg border border-primary/20">
                  <p className="text-xs text-primary mb-1 font-medium">ROC-AUC</p>
                  <p className="text-xl font-headline font-bold text-primary">0.941</p>
                </div>
              </div>
            </div>
            
            {/* Feature Importance */}
            <div>
              <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider mb-4 border-b border-outline-variant/40 pb-2">Feature Importance (Log Odds)</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-on-surface font-medium">Payment History</span>
                    <span className="text-on-surface-variant">2.45</span>
                  </div>
                  <div className="w-full bg-surface-variant h-2 rounded-full overflow-hidden">
                    <div className="bg-primary h-full rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-on-surface font-medium">Credit Utilization</span>
                    <span className="text-on-surface-variant">1.82</span>
                  </div>
                  <div className="w-full bg-surface-variant h-2 rounded-full overflow-hidden">
                    <div className="bg-primary/80 h-full rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-on-surface font-medium">Debt-to-Income</span>
                    <span className="text-on-surface-variant">1.24</span>
                  </div>
                  <div className="w-full bg-surface-variant h-2 rounded-full overflow-hidden">
                    <div className="bg-primary/60 h-full rounded-full" style={{ width: '45%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column Stack */}
        <div className="lg:col-span-4 flex flex-col gap-8">
          {/* Model Diagnostics */}
          <div className="bg-surface-container-low rounded-2xl p-6 border border-outline-variant/60 shadow-sahara-soft">
            <h2 className="text-lg font-headline font-semibold text-on-surface mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary text-sm">troubleshoot</span>
              Factor Model Diagnostics
            </h2>
            <div className="flex gap-4 mb-4">
              <div className="flex-1 bg-surface-bright rounded-xl p-4 border border-outline-variant/40 text-center">
                <p className="text-xs text-on-surface-variant mb-1 uppercase tracking-wide">R-Squared</p>
                <p className="text-2xl font-headline font-semibold text-on-surface">{rSquared.toFixed(3)}</p>
              </div>
              <div className="flex-1 bg-surface-bright rounded-xl p-4 border border-outline-variant/40 text-center">
                <p className="text-xs text-on-surface-variant mb-1 uppercase tracking-wide">Adj. R-Squared</p>
                <p className="text-2xl font-headline font-semibold text-on-surface">{adjRSquared.toFixed(3)}</p>
              </div>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Model explains {(rSquared * 100).toFixed(1)}% of variance in portfolio returns. Durbin-Watson statistic (1.92) indicates no significant autocorrelation.
            </p>
          </div>

          {/* A/B Testing Simulator */}
          <div className="bg-surface-container-low rounded-2xl p-6 border border-outline-variant/60 shadow-sahara-soft flex-1 flex flex-col">
            <h2 className="text-lg font-headline font-semibold text-on-surface mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-sm">compare_arrows</span>
              Strategy Evaluation
            </h2>
            <p className="text-sm text-on-surface-variant mb-6">Compare alternative factor loadings against baseline strategy.</p>
            <div className="bg-surface-bright border border-outline-variant/40 rounded-xl p-4 mb-4 relative overflow-hidden">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-tertiary"></div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-on-surface">Hypothesis Test</span>
                <span className="text-xs font-semibold text-tertiary bg-tertiary-container/30 px-2 py-0.5 rounded">Statistically Significant</span>
              </div>
              <div className="flex justify-between items-end">
                <div>
                  <p className="text-xs text-on-surface-variant">Z-Score</p>
                  <p className="font-headline text-lg font-semibold text-on-surface">3.42</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-on-surface-variant">p-value</p>
                  <p className="font-headline text-lg font-semibold text-on-surface">&lt; 0.001</p>
                </div>
              </div>
            </div>
            <div className="mt-auto">
              <button className="w-full bg-surface-variant hover:bg-outline-variant/40 text-on-surface-variant font-medium py-2.5 px-4 rounded-lg text-sm transition-colors border border-outline-variant/50 flex justify-center items-center gap-2">
                <span className="material-symbols-outlined text-sm">science</span>
                Run Simulation
              </button>
            </div>
          </div>
        </div>

        {/* Multiple Linear Regression (Alpha Generation) - Full Width Bottom */}
        <div className="lg:col-span-12 bg-surface-container-low rounded-2xl p-8 border border-outline-variant/60 shadow-sahara-soft mt-4">
          <div className="flex justify-between items-end mb-6 border-b border-outline-variant/40 pb-4">
            <div>
              <h2 className="text-2xl font-headline font-semibold text-on-surface mb-1 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">ssid_chart</span>
                Multiple Linear Regression: Alpha Generation
              </h2>
              <p className="text-sm text-on-surface-variant">Macroeconomic Factor Sensitivity Analysis</p>
            </div>
            <button className="text-sm text-primary font-medium hover:underline flex items-center gap-1">
              Export Data <span className="material-symbols-outlined text-sm">download</span>
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="py-3 px-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/50">Factor</th>
                  <th className="py-3 px-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/50 text-right">Coefficient (β)</th>
                  <th className="py-3 px-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/50 text-right">Std. Error</th>
                  <th className="py-3 px-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/50 text-right">t-stat</th>
                  <th className="py-3 px-4 text-xs font-semibold text-on-surface-variant uppercase tracking-wider border-b border-outline-variant/50 text-right">p-value</th>
                </tr>
              </thead>
              <tbody className="text-sm divide-y divide-outline-variant/30">
                <tr className="hover:bg-surface-variant/30 transition-colors">
                  <td className="py-4 px-4 font-medium text-on-surface flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                    Interest Rates (10Y T-Bill)
                  </td>
                  <td className="py-4 px-4 text-right font-headline">-1.245</td>
                  <td className="py-4 px-4 text-right text-on-surface-variant">0.182</td>
                  <td className="py-4 px-4 text-right font-medium">-6.84</td>
                  <td className="py-4 px-4 text-right text-tertiary font-medium">0.0001 **</td>
                </tr>
                <tr className="hover:bg-surface-variant/30 transition-colors">
                  <td className="py-4 px-4 font-medium text-on-surface flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-secondary"></div>
                    Inflation (CPI Core)
                  </td>
                  <td className="py-4 px-4 text-right font-headline">-0.876</td>
                  <td className="py-4 px-4 text-right text-on-surface-variant">0.210</td>
                  <td className="py-4 px-4 text-right font-medium">-4.17</td>
                  <td className="py-4 px-4 text-right text-tertiary font-medium">0.0024 *</td>
                </tr>
                <tr className="hover:bg-surface-variant/30 transition-colors">
                  <td className="py-4 px-4 font-medium text-on-surface flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-tertiary-container"></div>
                    GDP Growth (QoQ)
                  </td>
                  <td className="py-4 px-4 text-right font-headline">2.104</td>
                  <td className="py-4 px-4 text-right text-on-surface-variant">0.450</td>
                  <td className="py-4 px-4 text-right font-medium">4.67</td>
                  <td className="py-4 px-4 text-right text-tertiary font-medium">0.0011 **</td>
                </tr>
                <tr className="hover:bg-surface-variant/30 transition-colors">
                  <td className="py-4 px-4 font-medium text-on-surface flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-outline"></div>
                    Market Volatility (VIX)
                  </td>
                  <td className="py-4 px-4 text-right font-headline">-0.342</td>
                  <td className="py-4 px-4 text-right text-on-surface-variant">0.085</td>
                  <td className="py-4 px-4 text-right font-medium">-4.02</td>
                  <td className="py-4 px-4 text-right text-on-surface-variant">0.0450</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 flex items-center gap-4 text-xs text-on-surface-variant">
            <span>Significance levels:</span>
            <span className="flex items-center gap-1">** p &lt; 0.01</span>
            <span className="flex items-center gap-1">* p &lt; 0.05</span>
          </div>
        </div>
      </div>
    </main>
  );
};
