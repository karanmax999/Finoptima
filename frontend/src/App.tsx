import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';
import { 
  ExecutiveDashboard, 
  MarketRisk, 
  PortfolioCorrelation, 
  PredictiveModeling, 
  AssetAllocation, 
  StressTesting, 
  RiskReport 
} from './pages/Pages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<ExecutiveDashboard />} />
          <Route path="market-risk" element={<MarketRisk />} />
          <Route path="portfolio-correlation" element={<PortfolioCorrelation />} />
          <Route path="predictive-modeling" element={<PredictiveModeling />} />
          <Route path="asset-allocation" element={<AssetAllocation />} />
          <Route path="stress-test" element={<StressTesting />} />
          <Route path="risk-report" element={<RiskReport />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
