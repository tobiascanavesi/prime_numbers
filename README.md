# A Causal Light-Cone Theory of Primes

This repository contains the code implementation for the paper "A Causal Light–Cone Theory of Primes and a New Second–Order Term in Twin–Prime Asymptotics" by Tobías Canavesi.

## Abstract

We present the *Causal Prime Generation* (CPG) algorithm, prove its completeness, and model prime gaps via "light–cone" overlaps on the integer line. Besides recovering the classical Hardy–Littlewood twin-prime density 2C₂/(ln p)², we derive a computable second-order correction constant B≈0.0031591 arising from triple-cone intersections. Computations up to the millionth prime support the conjectural refinement:

Pr_twin(p) = 2C₂/(ln p)² + B/(ln p)² + o((ln p)⁻²)

## Repository Contents

- `cpg_algorithm.py` - Implementation of the Causal Prime Generation algorithm
- `cpg_physics.py` - Analysis of prime gap velocities with logarithmic fitting
- `space_time_diagram.py` - Visualization of the CPG algorithm's "light cones"
- `s3_estimation.py` - Estimation of the triple-overlap sum (S3) constant B

## Installation

To run the code in this repository, you'll need Python 3.8+ and the following dependencies:

```bash
pip install numpy matplotlib scipy sympy
```

## Usage
### Generating Primes with CPG
```bash
from cpg_algorithm import generate_primes_cpg

# Generate primes and their gaps using the CPG algorithm
primes, gaps = generate_primes_cpg(iterations=5000, max_multiple=100_000)
```

### Estimating the S3 Constant
Run s3_estimation.py to calculate the triple-overlap sum and estimate the B constant:
```bash
python s3_estimation.py
```

### Analyzing Prime Gap Velocities
Run cpg_physics.py to compute and fit the average prime gap velocity:
```bash
python cpg_physics.py
```

### Visualizing Light Cones
Run space_time_diagram.py to generate a visualization of the CPG algorithm's light cones:
```bash
python space_time_diagram.py
```

## The CPG Algorithm

The Causal Prime Generation (CPG) algorithm models prime number generation through a causal process where each discovered prime creates a "light cone" of its multiples. The algorithm:

- Starts with a seed set of known primes
- Generates all multiples of known primes up to a specified limit
- Finds the next prime as the first integer gap > 1 in the sorted list of multiples
- Repeats the process iteratively

This approach provides new insights into the distribution of primes and prime gaps.

## Citation

If you use this code in your research, please cite the original paper:
```
@article{canavesi2025causal,
  title={A Causal Light--Cone Theory of Primes and a New Second--Order Term in Twin--Prime Asymptotics},
  author={Canavesi, Tob\'{i}as},
  journal={},
  year={2025}
}
```
