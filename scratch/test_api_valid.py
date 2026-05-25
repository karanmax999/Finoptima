"""
test_api_valid.py
Validates all three FinOptima API endpoints against the live backend.
Run: python scratch/test_api_valid.py
"""

import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8080"

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

results = []


def post(path: str, payload: dict) -> tuple[int, dict]:
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            body = json.loads(raw) if raw else {"detail": f"HTTP {e.code} with empty body"}
        except Exception:
            body = {"detail": raw.decode(errors="replace")}
        return e.code, body


def check(label: str, status: int, body: dict, required_keys: list[str]):
    ok = status == 200 and all(k in body for k in required_keys)
    tag = PASS if ok else FAIL
    print(f"{tag} {label}  (HTTP {status})")
    if not ok:
        missing = [k for k in required_keys if k not in body]
        if missing:
            print(f"       Missing keys: {missing}")
        if "detail" in body:
            print(f"       Error detail: {body['detail']}")
    else:
        for k in required_keys:
            val = body[k]
            preview = str(val)[:80] + "..." if len(str(val)) > 80 else str(val)
            print(f"       {k}: {preview}")
    results.append(ok)
    print()


# ── 1. Distribution Fit ──────────────────────────────────────────────────────
print(f"{INFO} Testing POST /api/v1/risk/fit-distribution")
import random
random.seed(42)
returns_sample = [random.gauss(0.001, 0.02) for _ in range(252)]

status, body = post("/api/v1/risk/fit-distribution", {"returns": returns_sample})
check(
    "fit-distribution",
    status, body,
    ["status", "normal_fit", "lognormal_fit", "aic_comparison"]
)

# ── 2. Bayesian Credit Scoring ───────────────────────────────────────────────
print(f"{INFO} Testing POST /api/v1/risk/bayesian-credit")
status, body = post("/api/v1/risk/bayesian-credit", {
    "prior_default": 0.05,
    "income": 75000.0,
    "credit_score": 720.0,
    "term": 36
})
check(
    "bayesian-credit",
    status, body,
    ["status", "posterior_probability", "prior_baseline", "feature_importance_kl"]
)

# ── 3. Portfolio Optimization (fallback dataset) ─────────────────────────────
print(f"{INFO} Testing POST /api/v1/portfolio/optimize  (fallback synthetic data)")
status, body = post("/api/v1/portfolio/optimize", {
    "risk_free_rate": 0.02,
    "max_concentration_constraint": 0.40,
    "min_return_constraint": None
})
check(
    "portfolio/optimize",
    status, body,
    ["status", "tickers", "expected_returns", "markowitz", "linear_programming",
     "simplex_diagnostics", "regression_diagnostics", "risk_metrics"]
)

# ── Summary ──────────────────────────────────────────────────────────────────
passed = sum(results)
total  = len(results)
print("=" * 50)
if passed == total:
    print(f"\033[92mAll {total}/{total} tests passed.\033[0m")
    sys.exit(0)
else:
    print(f"\033[91m{passed}/{total} tests passed. See failures above.\033[0m")
    sys.exit(1)
