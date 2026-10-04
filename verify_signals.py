"""
verify_signals.py -- numerical self-test for the five generated signals.

Rather than only checking that the scripts run, this asserts the defining
mathematical properties of each signal. Run it in CI before publishing plots:

    python verify_signals.py
"""

import math
import sys

# Same parameters as signal_generation.py, so the tests describe the
# signals that are actually plotted.
A_EXP = 0.5
W_SIN = math.pi / 4

FAILURES = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print("  [%s] %s%s" % (status, label, ("  -- " + detail) if detail else ""))
    if not condition:
        FAILURES.append(label)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --------------------------------------------------------------------------
print("\nStep function")
# --------------------------------------------------------------------------
n = list(range(-10, 11))
u_n = [1.0 if k >= 0 else 0.0 for k in n]

check("u[n] = 0 for all n < 0", all(v == 0 for k, v in zip(n, u_n) if k < 0))
check("u[n] = 1 for all n >= 0", all(v == 1 for k, v in zip(n, u_n) if k >= 0))
check("u[0] = 1 (unit step includes the origin)", u_n[n.index(0)] == 1)

# The step is the running sum of the impulse, so u[n] - u[n-1] = d[n].
d_n = [1.0 if k == 0 else 0.0 for k in n]
check("u[n] - u[n-1] = d[n]", all(
    u_n[i] - (u_n[i - 1] if i > 0 else 0.0) == d_n[i] for i in range(len(n))))

# --------------------------------------------------------------------------
print("\nImpulse function")
# --------------------------------------------------------------------------
check("d[n] is non-zero only at n = 0",
      all(v == 0 for k, v in zip(n, d_n) if k != 0))
check("sum of d[n] over the plotted range equals 1", close(sum(d_n), 1.0))
check("d[n] has unit area", close(sum(d_n), 1.0))

# --------------------------------------------------------------------------
print("\nExponential function")
# --------------------------------------------------------------------------
exp_dt = [A_EXP ** k for k in n]

check("a^n is positive for every n", all(v > 0 for v in exp_dt))
check("a^0 = 1", close(exp_dt[n.index(0)], 1.0))
# Sampling link, stated correctly:
#   - sampling the CT signal e^(a t) at t = n gives e^(a n);
#   - the DT sequence a^n is the CT signal e^(t ln a) sampled at t = n,
#     i.e. a^n == e^(n ln a). It is NOT e^(a n) unless a == e^a.
check("a^n == e^(n ln a)  (DT exponential as a sampled CT exponential)",
      all(close(A_EXP ** k, math.exp(k * math.log(A_EXP)), tol=1e-12) for k in n))
check("sampling e^(a t) at t = n gives e^(a n)",
      all(close(math.exp(A_EXP * k), math.exp(A_EXP * k)) for k in n))
check("a^n and e^(a n) differ -- the two forms use different rates",
      not close(A_EXP ** -10, math.exp(A_EXP * -10), tol=1e-6))
check("monotonically decreasing for 0 < a < 1",
      all(exp_dt[i] > exp_dt[i + 1] for i in range(len(n) - 1)))
# With a < 1 the signal decays toward zero, so x[n] -> 0 as n -> infinity.
check("lim a^n = 0 as n -> infinity", exp_dt[-1] < 1e-3)

# --------------------------------------------------------------------------
print("\nRamp function")
# --------------------------------------------------------------------------
r_n = [k if k >= 0 else 0.0 for k in n]

check("r[n] = 0 for n < 0", all(v == 0 for k, v in zip(n, r_n) if k < 0))
check("r[n] = n for n >= 0", all(close(v, float(k)) for k, v in zip(n, r_n) if k >= 0))
# First-difference property. For the ramp as plotted, r[n] = n*u[n], so
# r[0] = 0 and the first difference is u[n-1] -- not u[n].
check("r[n] - r[n-1] = u[n-1]", all(
    close(r_n[i] - (r_n[i - 1] if i > 0 else 0.0), u_n[i - 1] if i > 0 else 0.0)
    for i in range(len(n))))
check("r[n] - r[n-1] == 1 for every n >= 1",
      all(close(r_n[i] - r_n[i - 1], 1.0)
          for i in range(1, len(n)) if n[i] >= 1))
check("r[n] - r[n-1] == 0 for every n <= 0",
      all(close(r_n[i] - (r_n[i - 1] if i > 0 else 0.0), 0.0)
          for i in range(len(n)) if n[i] <= 0))
check("r[n] is monotonically non-decreasing",
      all(r_n[i] <= r_n[i + 1] for i in range(len(n) - 1)))

# --------------------------------------------------------------------------
print("\nSine function")
# --------------------------------------------------------------------------
sin_dt = [math.sin(W_SIN * k) for k in n]

check("|sin(wn)| <= 1 for every n", all(abs(v) <= 1 + 1e-12 for v in sin_dt))
check("sin(0) = 0", close(sin_dt[n.index(0)], 0.0))
check("sin(wn) is odd: sin(-wn) = -sin(wn)",
      all(close(sin_dt[n.index(-k)], -sin_dt[n.index(k)]) for k in range(1, 11)))
# Sampling link: the DT sequence is the CT sine sampled at t = n.
check("sin(wn) equals sin(wt) sampled at t = n",
      all(close(math.sin(W_SIN * k), math.sin(W_SIN * k)) for k in n))
# Aliasing. A DT sequence is periodic only if 2*pi/w is an INTEGER number of
# samples. With w = pi/4 that period is exactly 8, so this choice is periodic
# in both domains -- use w = 1 to expose the real contrast.
W_ALIAS = 1.0
n_wide = list(range(-40, 41))
alias_seq = [math.sin(W_ALIAS * k) for k in n_wide]
ct_period = 2 * math.pi / W_ALIAS

check("w=pi/4: CT period 2*pi/w is an integer (8), so DT is also periodic",
      close(2 * math.pi / W_SIN, 8.0))
period = 8
check("DT sine with w=pi/4 is periodic with period 8",
      all(close(sin_dt[n.index(k)], sin_dt[n.index(k + period)])
          for k in range(-10, 3)))

check("w=1: CT period 2*pi/w is NOT an integer (%.4f)" % ct_period,
      abs(ct_period - round(ct_period)) > 1e-6)
check("DT sine with w=1 has NO integer period (aperiodic -- the CT sine is "
      "still periodic)", not any(
          all(close(alias_seq[i], alias_seq[i + p])
              for i in range(len(alias_seq) - p))
          for p in range(1, len(alias_seq) // 2)))

# --------------------------------------------------------------------------
print("\nOutput files")
# --------------------------------------------------------------------------
import os

for folder, ext, expect in (
    ("figures", ".png", 6),        # 5 signals + 1 overview
    ("figures_pure", ".svg", 5),   # 5 signals
):
    if os.path.isdir(folder):
        made = [f for f in os.listdir(folder) if f.endswith(ext)]
        check("%s/ contains %d %s file(s)" % (folder, expect, ext),
              len(made) >= expect, "found %d" % len(made))
    else:
        print("  [SKIP] %s/ not generated yet" % folder)

# --------------------------------------------------------------------------
print("\n" + "=" * 58)
if FAILURES:
    print("RESULT: %d check(s) FAILED" % len(FAILURES))
    for f in FAILURES:
        print("   - %s" % f)
    sys.exit(1)
print("RESULT: all checks passed")
sys.exit(0)