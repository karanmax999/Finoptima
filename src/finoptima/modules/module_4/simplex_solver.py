"""
Step-by-step Simplex and Two-Phase Simplex Solver for Portfolio LPP.
Tracks and exports exact tableau matrices, basic/non-basic variables, and pivot operations.
"""

import numpy as np
from typing import Dict, List, Tuple, Union

class SimplexSolver:
    """
    Simplex Solver for Linear Programming.
    Solves Max c^T x s.t. Ax <= b, x >= 0
    Supports tracking exact iterations and tableaus.
    """
    
    def __init__(self, c: np.ndarray, A: np.ndarray, b: np.ndarray):
        """
        Initialize standard maximization Simplex solver:
        Maximize z = c^T x
        s.t. Ax <= b, x >= 0
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        
        self.n_vars = len(c)
        self.n_constraints = len(b)
        
        # Dimensions of tableau:
        # Rows: n_constraints + 1 (last row is objective function)
        # Columns: n_vars (decision) + n_constraints (slack) + 1 (RHS)
        self.tableau = np.zeros((self.n_constraints + 1, self.n_vars + self.n_constraints + 1))
        
        # Populate tableau
        # Constraints coefficients
        self.tableau[:self.n_constraints, :self.n_vars] = self.A
        # Slack variables identity matrix
        self.tableau[:self.n_constraints, self.n_vars:self.n_vars + self.n_constraints] = np.eye(self.n_constraints)
        # RHS
        self.tableau[:self.n_constraints, -1] = self.b
        # Objective row (z - c^T x = 0) => coeff is -c
        self.tableau[-1, :self.n_vars] = -self.c
        self.tableau[-1, -1] = 0.0
        
        # Keep track of basic variables for each row (indices of variables)
        # Initially, slack variables (indices n_vars to n_vars + n_constraints - 1) are basic
        self.basic_vars = [self.n_vars + i for i in range(self.n_constraints)]
        self.iterations = []
        
    def _get_tableau_state(self) -> Dict:
        """Captures the current state of the tableau."""
        headers = [f"x_{i+1}" for i in range(self.n_vars)] + \
                  [f"s_{i+1}" for i in range(self.n_constraints)] + \
                  ["RHS"]
        
        row_names = [f"Row {i+1} (Basic: {headers[self.basic_vars[i]]})" for i in range(self.n_constraints)] + ["Obj Row (z)"]
        
        return {
            "matrix": self.tableau.tolist(),
            "headers": headers,
            "row_names": row_names,
            "basic_variables": [headers[idx] for idx in self.basic_vars],
            "objective_value": float(self.tableau[-1, -1])
        }

    def solve(self, max_iter: int = 50) -> Dict:
        """Runs the Simplex algorithm tracking all iterations."""
        self.iterations = []
        self.iterations.append({
            "step": 0,
            "tableau": self._get_tableau_state(),
            "pivot": None,
            "message": "Initial Tableau Setup"
        })
        
        for step in range(1, max_iter + 1):
            # Check for optimality (all elements in objective row, excluding RHS, are >= 0)
            obj_row = self.tableau[-1, :-1]
            if np.all(obj_row >= -1e-9):
                # Optimal solution found
                weights = np.zeros(self.n_vars)
                for row_idx, var_idx in enumerate(self.basic_vars):
                    if var_idx < self.n_vars:
                        weights[var_idx] = self.tableau[row_idx, -1]
                
                return {
                    "status": "Optimal",
                    "iterations": self.iterations,
                    "weights": weights.tolist(),
                    "optimal_return": float(self.tableau[-1, -1]),
                    "message": "Optimal solution found successfully."
                }
            
            # Select entering variable (most negative coefficient in obj row)
            entering_col = np.argmin(obj_row)
            
            # Check for unboundedness (all elements in entering column are <= 0)
            col_vals = self.tableau[:-1, entering_col]
            if np.all(col_vals <= 1e-9):
                return {
                    "status": "Unbounded",
                    "iterations": self.iterations,
                    "weights": [],
                    "optimal_return": 0.0,
                    "message": "Problem is unbounded."
                }
            
            # Select leaving variable (minimum ratio test RHS / coefficient)
            ratios = []
            valid_rows = []
            for row_idx in range(self.n_constraints):
                val = self.tableau[row_idx, entering_col]
                if val > 1e-9:
                    ratio = self.tableau[row_idx, -1] / val
                    ratios.append(ratio)
                    valid_rows.append(row_idx)
            
            if not ratios:
                return {
                    "status": "Infeasible",
                    "iterations": self.iterations,
                    "weights": [],
                    "optimal_return": 0.0,
                    "message": "No valid pivot row (problem might be infeasible)."
                }
                
            leaving_row = valid_rows[np.argmin(ratios)]
            pivot_val = self.tableau[leaving_row, entering_col]
            
            # Log pivot information before pivoting
            pivot_info = {
                "entering_var": self.iterations[0]["tableau"]["headers"][entering_col],
                "leaving_var": self.iterations[0]["tableau"]["headers"][self.basic_vars[leaving_row]],
                "pivot_row": int(leaving_row),
                "pivot_col": int(entering_col),
                "pivot_value": float(pivot_val)
            }
            
            # Perform row operations (pivoting)
            # Normalize pivot row
            self.tableau[leaving_row] /= pivot_val
            
            # Eliminate other rows
            for r in range(self.n_constraints + 1):
                if r != leaving_row:
                    factor = self.tableau[r, entering_col]
                    self.tableau[r] -= factor * self.tableau[leaving_row]
            
            # Update basic variables
            self.basic_vars[leaving_row] = entering_col
            
            # Save iteration
            self.iterations.append({
                "step": step,
                "tableau": self._get_tableau_state(),
                "pivot": pivot_info,
                "message": f"Pivoted: Entering {pivot_info['entering_var']}, Leaving {pivot_info['leaving_var']}"
            })
            
        return {
            "status": "MaxIterations",
            "iterations": self.iterations,
            "weights": [],
            "optimal_return": 0.0,
            "message": "Reached maximum iterations without finding optimal solution."
        }
