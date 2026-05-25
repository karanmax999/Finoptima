import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { TrendingUp } from 'lucide-react';

export const FrontierChart: React.FC = () => {
  const { apiResults } = useFinoptimaStore();
  
  if (!apiResults || !apiResults.markowitz) {
    return (
      <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-6 rounded-2xl h-[380px] flex items-center justify-center">
        <p className="text-slate-500 font-mono text-xs">Computing optimization model diagnostics...</p>
      </div>
    );
  }

  const { frontier, max_sharpe, min_volatility, risk_parity } = apiResults.markowitz;

  const chartData = frontier.map((p) => ({
    x: parseFloat((p.volatility * 100).toFixed(4)),
    y: parseFloat((p.return * 100).toFixed(4)),
    z: 1,
    name: 'Frontier Curve'
  }));

  // Add optimal highlights
  const scatterPoints = [
    {
      x: parseFloat((max_sharpe.volatility * 100).toFixed(4)),
      y: parseFloat((max_sharpe.return * 100).toFixed(4)),
      z: 6,
      name: 'Max Sharpe Portfolio',
      color: '#22C55E' // Green
    },
    {
      x: parseFloat((min_volatility.volatility * 100).toFixed(4)),
      y: parseFloat((min_volatility.return * 100).toFixed(4)),
      z: 6,
      name: 'Minimum Volatility',
      color: '#3B82F6' // Blue
    },
    {
      x: parseFloat((risk_parity.volatility * 100).toFixed(4)),
      y: parseFloat((risk_parity.return * 100).toFixed(4)),
      z: 6,
      name: 'Risk Parity Allocator',
      color: '#EC4899' // Pink/Magenta
    }
  ];

  const fullData = [...chartData, ...scatterPoints];

  return (
    <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-6 rounded-2xl h-[380px] flex flex-col justify-between">
      <div>
        <h3 className="text-sm font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2 mb-1">
          <TrendingUp size={14} className="text-indigo-400" /> Modern Portfolio Efficient Frontier
        </h3>
        <p className="text-xxs text-slate-500 font-mono mb-4">
          Visualizing expected return against volatility with calculated risk bounds.
        </p>
      </div>

      <div className="h-[270px]">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
            <XAxis
              type="number"
              dataKey="x"
              name="Volatility"
              unit="%"
              stroke="#475569"
              tick={{ fontSize: 9, fontFamily: 'monospace' }}
              label={{ value: 'Volatility (Standard Deviation)', position: 'insideBottom', offset: -10, fill: '#64748B', fontSize: 9, fontFamily: 'monospace' }}
            />
            <YAxis
              type="number"
              dataKey="y"
              name="Return"
              unit="%"
              stroke="#475569"
              tick={{ fontSize: 9, fontFamily: 'monospace' }}
              label={{ value: 'Expected Return', angle: -90, position: 'insideLeft', offset: 0, fill: '#64748B', fontSize: 9, fontFamily: 'monospace' }}
            />
            <ZAxis type="number" dataKey="z" range={[30, 200]} />
            <Tooltip
              cursor={{ strokeDasharray: '3 3', stroke: '#1e293b' }}
              contentStyle={{
                backgroundColor: '#0B0F19',
                borderColor: '#1E293B',
                color: '#FFF',
                fontFamily: 'monospace',
                fontSize: '11px',
                borderRadius: '8px'
              }}
            />
            <Scatter name="Frontier Portfolios" data={fullData}>
              {fullData.map((entry: any, index: number) => {
                if (entry.name === 'Max Sharpe Portfolio') return <Cell key={`cell-${index}`} fill="#22C55E" />;
                if (entry.name === 'Minimum Volatility') return <Cell key={`cell-${index}`} fill="#3B82F6" />;
                if (entry.name === 'Risk Parity Allocator') return <Cell key={`cell-${index}`} fill="#EC4899" />;
                return <Cell key={`cell-${index}`} fill="#6366F1" opacity={0.35} />;
              })}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* legend overlays */}
      <div className="flex justify-center gap-6 mt-2 text-xxs font-mono text-slate-400">
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          <span>Max Sharpe ({(max_sharpe.return * 100).toFixed(1)}%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
          <span>Min Vol ({(min_volatility.return * 100).toFixed(1)}%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-pink-500" />
          <span>Risk Parity</span>
        </div>
      </div>
    </div>
  );
};
export default FrontierChart;
