import { create } from 'zustand';

// [Types remaining the same as before...]
export interface SimplexIteration {
  step: number;
  tableau: {
    matrix: number[][];
    headers: string[];
    row_names: string[];
    basic_variables: string[];
    objective_value: number;
  };
  pivot: {
    entering_var: string;
    leaving_var: string;
    pivot_row: number;
    pivot_col: number;
    pivot_value: number;
  } | null;
  message: string;
}

export interface ApiResults {
  tickers: string[];
  expected_returns: number[];
  volatilities: number[];
  risk_metrics: {
    covariance_matrix: number[][];
    correlation_matrix: number[][];
    var_historical_95: number;
    var_parametric_95: number;
    cvar_historical_95: number;
  };
  markowitz: {
    max_sharpe: {
      weights: Record<string, number>;
      return: number;
      volatility: number;
      sharpe_ratio: number;
    };
    min_volatility: {
      weights: Record<string, number>;
      return: number;
      volatility: number;
    };
    risk_parity: {
      weights: Record<string, number>;
      return: number;
      volatility: number;
    };
    frontier: Array<{
      volatility: number;
      return: number;
      weights: Record<string, number>;
    }>;
  };
  linear_programming: {
    weights: Record<string, number>;
    return: number;
    status: string;
  };
  simplex_diagnostics: {
    solver_status: string;
    weights: Record<string, number>;
    optimal_return: number;
    iterations: SimplexIteration[];
    message: string;
  };
  regression_diagnostics: {
    r_squared: number;
    adjusted_r_squared: number;
    rmse: number;
    mae: number;
    coefficients: Record<string, number>;
    intercept: number;
    p_values: Record<string, number>;
  };
}

export interface BayesianResults {
  posterior_probability: number;
  prior_baseline: number;
  feature_importance_kl: Record<string, number>;
  transparency_meta: {
    n_bins: number;
    smoothing: number;
    feature_distributions: Record<string, {
      given_default: number[];
      given_no_default: number[];
    }>;
  };
}

interface FinoptimaState {
  tickers: string[];
  returnsData: number[][] | null;
  
  // Bayesian priors
  priorDefault: number;
  borrowerIncome: number;
  borrowerCreditScore: number;
  borrowerTerm: number;

  // LPP constraints
  minReturnConstraint: number;
  maxConcentration: number;
  riskFreeRate: number;

  // App States
  isCalculating: boolean;
  isUploading: boolean;
  apiResults: ApiResults | null;
  bayesianResults: BayesianResults | null;
  csvUploadMessage: string | null;
  error: string | null;

  // Setters & Actions
  setPriorDefault: (val: number) => void;
  setLppConstraints: (minRet: number, maxConc: number) => void;
  setBorrowerProfile: (income: number, score: number, term: number) => void;
  fetchOptimization: () => Promise<void>;
  fetchBayesianScoring: () => Promise<void>;
  uploadCsv: (file: File) => Promise<void>;
  clearCache: () => void;
}

// Mock data removed. Real data will be fetched from the FastAPI backend.

// Mock Bayesian results removed. Real results will be fetched from the FastAPI backend.

export const useFinoptimaStore = create<FinoptimaState>((set, get) => ({
  tickers: ['AAPL', 'MSFT', 'TSLA', 'SPY'],
  returnsData: null,
  
  priorDefault: 0.05,
  borrowerIncome: 75000,
  borrowerCreditScore: 720,
  borrowerTerm: 36,

  minReturnConstraint: 0.04,
  maxConcentration: 0.40,
  riskFreeRate: 0.02,

  isCalculating: false,
  isUploading: false,
  apiResults: null,
  bayesianResults: null,
  csvUploadMessage: null,
  error: null,

  setPriorDefault: (val) => {
    set({ priorDefault: val });
  },

  setLppConstraints: (minRet, maxConc) => {
    set({ minReturnConstraint: minRet, maxConcentration: maxConc });
  },

  setBorrowerProfile: (income, score, term) => {
    set({ borrowerIncome: income, borrowerCreditScore: score, borrowerTerm: term });
  },

  fetchOptimization: async () => {
  set({ isCalculating: true, error: null });
  try {
    const baseUrl = 'http://127.0.0.1:8080';
    const payload = {
      tickers: get().tickers,
      returns: get().returnsData,
      risk_free_rate: get().riskFreeRate,
      max_concentration_constraint: get().maxConcentration,
      min_return_constraint: get().minReturnConstraint
    };
    const response = await fetch(`${baseUrl}/api/v1/portfolio/optimize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      throw new Error(`Optimization request failed: ${response.status}`);
    }
    const data = await response.json();
    set({ apiResults: data, isCalculating: false });
  } catch (e) {
    set({ error: e instanceof Error ? e.message : String(e), isCalculating: false });
  }
},

  fetchBayesianScoring: async () => {
  try {
    const baseUrl = 'http://127.0.0.1:8080';
    const payload = {
      prior_default: get().priorDefault,
      income: get().borrowerIncome,
      credit_score: get().borrowerCreditScore,
      term: get().borrowerTerm
    };
    const response = await fetch(`${baseUrl}/api/v1/risk/bayesian-credit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      throw new Error(`Bayesian scoring failed: ${response.status}`);
    }
    const data = await response.json();
    set({ bayesianResults: data });
  } catch (e) {
    set({ error: e instanceof Error ? e.message : String(e) });
  }
},

  uploadCsv: async (file) => {
    set({ isUploading: true, csvUploadMessage: null, error: null });
    const baseUrl = 'http://127.0.0.1:8080';
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await fetch(`${baseUrl}/api/v1/data/upload-csv`, {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error(`CSV upload failed: ${response.status}`);
      }
      const data = await response.json();
      set({
        tickers: data.tickers || [],
        returnsData: data.returns || null,
        csvUploadMessage: data.message || 'CSV uploaded successfully',
        isUploading: false
      });
      await get().fetchOptimization();
    } catch (e) {
      set({ error: e instanceof Error ? e.message : String(e), isUploading: false });
    }
  },

  clearCache: () => {
    set({
      tickers: ['AAPL', 'MSFT', 'TSLA', 'SPY'],
      returnsData: null,
      csvUploadMessage: null,
      apiResults: null
    });
    get().fetchOptimization();
  }
}));
