import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

primes = [2, 3, 5]
colors = {2: "red", 3: "orange", 5: "green"}
steps = list(range(len(primes)))
fig, ax = plt.subplots(figsize=(6, 6))

for n, p in zip(steps, primes):
    ax.scatter(n, p, marker="x", color=colors[p], s=100, zorder=3)
    ax.text(n - 0.1, p, f"{p}", va="center", ha="right", fontsize=12, color=colors[p])

# Draw light-cone arrows and label eliminated multiples
for n, p in zip(steps, primes):
    color = colors[p]
    multiples = list(range(2 * p, p * p + 1, p))
    # Draw an arrow from (n, p) to (n+1, m) for each multiple m
    for m in multiples:
        arrow = FancyArrowPatch(
            (n, p),
            (n + 1, m),
            arrowstyle="->",
            mutation_scale=10,
            color=color,
            linewidth=1,
        )
        ax.add_patch(arrow)
    # Label the list of eliminated multiples next to the cluster
    y_mean = sum(multiples) / len(multiples)
    ax.text(
        n + 1 + 0.05,
        y_mean,
        ",".join(map(str, multiples)),
        va="center",
        color=color,
        fontsize=10,
    )

ax.set_xlim(-0.5, len(primes) + 0.5)
ax.set_ylim(0, primes[-1] ** 2 + 2)
ax.set_xlabel("CPG Step $n$")
ax.set_ylabel("Integer value")
ax.set_title("Spacetime Diagram of CPG Light Cones")
ax.grid(True, linestyle="dotted", linewidth=0.5)

plt.tight_layout()
plt.savefig("spacetime_diagram.pdf")
plt.show()
