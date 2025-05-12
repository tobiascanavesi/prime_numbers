import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange, prime

PATTERN = [2]  # twin‐prime offset
NS = [
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    2000,
    3000,
    4000,
    5000,
    6000,
    7000,
    8000,
    9000,
    10000,
    20000,
    30000,
    40000,
    50000,
    60000,
    70000,
    80000,
    90000,
    100000,
    200000,
    # extend as needed
]
BOOT_REPS = 100  # number of bootstrap replicates


def compute_g_vector(pattern, p_max):
    """Compute the g-vector for primes up to p_max given a pattern."""
    base = [0] + pattern
    return np.array(
        [len({(-a) % p for a in base}) / p**2 for p in primerange(3, p_max + 1)]
    )


def compute_S3_from_g(gs):
    """Compute the triple-overlap sum S3 from g-vector gs."""
    S1 = gs.sum()
    S2 = np.sum(gs**2)
    S3 = np.sum(gs**3)
    return (S1**3 - 3 * S1 * S2 + 2 * S3) / 6


# 1) Compute p_n and corresponding g-vectors & S3
p_ns = np.array([prime(n) for n in NS])
g_vectors = [compute_g_vector(PATTERN, p) for p in p_ns]
S3s = np.array([compute_S3_from_g(gs) for gs in g_vectors])

# 2) Estimate B by averaging the last few S3s
B_est = float(np.mean(S3s[-5:]))

# 3) Linear fit for residuals = S3(p_n) - B
x = 1.0 / np.log(np.log(p_ns))
resid = S3s - B_est
m_fit, c_fit = np.polyfit(x, resid, 1)

# 4) Bootstrap error bars
stds = []
for gs in g_vectors:
    samples = [
        compute_S3_from_g(np.random.choice(gs, size=len(gs), replace=True))
        for _ in range(BOOT_REPS)
    ]
    stds.append(np.std(samples))

# ---- PLOT A: Convergence of S3 ----
plt.figure(figsize=(6, 4))
plt.plot(np.log(np.log(p_ns)), S3s, "o-", label=r"$S_3(p_n)$")
plt.axhline(B_est, linestyle="--", label=rf"$B \approx {B_est:.6f}$")
plt.xlabel(r"$\ln\ln p_n$")
plt.ylabel(r"$S_3(p_n)$")
plt.title("Convergence of $S_3(p_n)$")
plt.legend()
plt.tight_layout()
plt.savefig("S3_convergence.pdf")
plt.show()

# ---- PLOT B: Residuals with Bootstrap Errors ----
plt.figure(figsize=(6, 4))
plt.errorbar(np.log(np.log(p_ns)), resid, yerr=stds, fmt="o", label="Residual")
plt.plot(
    np.log(np.log(p_ns)),
    m_fit * x + c_fit,
    "--",
    label=rf"Fit: $y={m_fit:.2e}x + {c_fit:.2e}$",
)
plt.xlabel(r"$\ln\ln p_n$")
plt.ylabel(r"$S_3(p_n) - B$")
plt.title("Residuals with Bootstrap Errors")
plt.legend()
plt.tight_layout()
plt.savefig("S3_errorbars.pdf")
plt.show()

# ---- PLOT C: Origin Fit on Tail (NS >= 2000) ----
mask = np.array(NS) >= 2000
x_tail = x[mask]
resid_tail = resid[mask]
m0 = np.dot(x_tail, resid_tail) / np.dot(x_tail, x_tail)

plt.figure(figsize=(6, 4))
plt.plot(x, resid, "o", label="Residual")
plt.plot(x_tail, m0 * x_tail, "-", label=rf"Origin fit: $y={m0:.2e}x$")
plt.xlabel(r"$1/\ln\ln p_n$")
plt.ylabel(r"$S_3(p_n) - B$")
plt.title("Residual vs $1/\\ln\\ln p_n$")
plt.savefig("S3_residual_origin.pdf")
plt.legend()
plt.tight_layout()
plt.show()
