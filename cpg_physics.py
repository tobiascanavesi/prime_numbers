import matplotlib.pyplot as plt
import numpy as np

from cpg_algorithm import (
    generate_primes_cpg,
    compute_average_gap_velocity,
    fit_log_model,
    log_model,
)

# 1) Generate primes and gaps
primes, gaps = generate_primes_cpg(iterations=5000, max_multiple=100_000)

# 2) Compute average gap velocity
window_size = 500
avg_vel = compute_average_gap_velocity(gaps, window_size)

# 3) Fit the log‐model
popt, _ = fit_log_model(avg_vel)
a_fit, b_fit, c_fit = popt
print(f"Fitted parameters: a={a_fit}, b={b_fit}, c={c_fit}")

# 4) Plot
x = np.arange(len(avg_vel))
plt.figure(figsize=(10, 6))
plt.plot(x, avg_vel, "bo", label="Avg Gap Velocity")
plt.plot(x, log_model(x, *popt), "r-", label="Logarithmic Fit")
plt.xlabel("Window Index")
plt.ylabel("Average Prime Gap Velocity")
plt.title("Logarithmic Fit to Average Prime Gap Velocity")
plt.legend()
plt.grid(True)
plt.show()
