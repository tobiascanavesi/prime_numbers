import numpy as np
from scipy.optimize import curve_fit


def generate_multiples(prime: int, max_multiple: int = 100_000) -> list[int]:
    """
    Generate all multiples of `prime` up to `max_multiple`.
    """
    multiples = []
    k = 1
    while True:
        m = k * prime
        if m > max_multiple:
            break
        multiples.append(m)
        k += 1
    return multiples


def initialize_primes() -> list[int]:
    """
    Seed the CPG algorithm with the first few primes.
    """
    return [2, 3, 5, 7]


def find_next_prime(unique_list: list[int]) -> int | None:
    """
    Find the next prime as the first integer gap >1 in `unique_list`.
    Returns None if no new prime is found.
    """
    for i in range(len(unique_list) - 1):
        gap = unique_list[i + 1] - unique_list[i]
        if gap > 1:
            candidate = unique_list[i] + 1
            # simple primality check
            for d in range(2, int(np.sqrt(candidate)) + 1):
                if candidate % d == 0:
                    break
            else:
                return candidate
    return None


def generate_primes_cpg(
    iterations: int = 5000, max_multiple: int = 100_000
) -> tuple[list[int], list[int]]:
    """
    Run the CPG algorithm for a given number of `iterations`, returning
    the full list of found primes and the gaps between successive primes.
    """
    primes = initialize_primes()
    gaps = []

    for _ in range(iterations):
        # 1) build the union of multiples of each known prime
        all_mults = set()
        for p in primes:
            all_mults.update(generate_multiples(p, max_multiple))

        unique_sorted = sorted(all_mults)

        # 2) find the next prime
        nxt = find_next_prime(unique_sorted)
        if nxt is None:
            break

        gaps.append(nxt - primes[-1])
        primes.append(nxt)

    return primes, gaps


def compute_average_gap_velocity(gaps: list[int], window_size: int = 500) -> np.ndarray:
    """
    Given a list of prime gaps, return the sliding‐window average gap
    velocities (one value per window).
    """
    n = len(gaps)
    if window_size > n:
        return np.array([])

    return np.array(
        [np.mean(gaps[i : i + window_size]) for i in range(n - window_size + 1)]
    )


def log_model(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """
    A three-parameter logarithmic model:  a * ln(b*x + c)
    """
    return a * np.log(b * x + c)


def fit_log_model(avg_vel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Fit `log_model` to `avg_vel` vs window‐index. Returns (popt, pcov).
    """
    x = np.arange(len(avg_vel))
    popt, pcov = curve_fit(log_model, x, avg_vel, maxfev=10_000)
    return popt, pcov
