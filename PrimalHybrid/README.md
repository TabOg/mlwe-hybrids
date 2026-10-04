# Primal Hybrid with Rotations Estimator

This directory contains an estimator for `RotPrimalHybrid`, a version of the Primal Hybrid attack which uses negacyclic rotations of a sparse secret in a power-of-two cyclotomic ring. It accompanies [*On the Concrete Hardness Gap Between MLWE and LWE*](https://eprint.iacr.org/2026/279).

The implementation is adapted from the `PrimalHybrid` class in the community [Lattice Estimator](https://github.com/malb/lattice-estimator). The lattice reduction and close vector parts of the estimate are unchanged. The difference is in the guessing set: if a length-`zeta` segment has probability `p` of having low enough weight, we approximate the probability that at least one of the `poly_degree` rotations has low enough weight by

```text
1 - (1 - p)^poly_degree.
```

The corresponding guessing set is `poly_degree` times larger. This estimator optimises the usual attack parameters around this new size/probability tradeoff.

## Setup

This code requires SageMath. The Lattice Estimator is included as a pinned submodule, so clone the repository recursively or initialise the submodules after cloning:

```bash
git clone --recurse-submodules https://github.com/TabOg/mlwe-hybrids.git
cd mlwe-hybrids/PrimalHybrid
```

or

```bash
git submodule update --init --recursive
cd PrimalHybrid
```

Run the scripts with Sage, for example:

```bash
sage sparse_estimates.py
```

Some of the larger parameter sets take a long time to estimate.

## Quick start

For the usual interface, construct an `LWE.Parameters` object for the coefficient embedding and call `estimate()`:

```python
from sage.all import oo

from lattice_estimator.estimator import LWE, ND
from lwe_rot_primal import estimate

logn = 13
logq = 99
h = 64

params = LWE.Parameters(
    n=2**logn,
    q=2**logq,
    Xs=ND.SparseTernary(p=h // 2, m=h // 2, n=2**logn),
    Xe=ND.DiscreteGaussian(stddev=3.2),
    m=oo,
)

estimates = estimate(params, poly_degree=2**logn)
for attack, cost in estimates.items():
    print(f"{attack}: {cost!r}")
```

`estimate()` returns two estimates:

- `bdd_hybrid` uses the projected-CVP model without a meet-in-the-middle speedup;
- `bdd_mitm_hybrid` uses Babai's Nearest Plane algorithm and the full square-root meet-in-the-middle heuristic from the paper.

This follows the Lattice Estimator [`LWE.estimate()` function](https://github.com/malb/lattice-estimator/blob/6019056011d10d7e9c30a0d5da2d2f729fbc2eec/estimator/lwe.py#L142-L156), which includes two primal hybrid variants: projected CVP without MitM (babai=False, mitm=False) and Babai’s Nearest Plane with MitM (babai=True, mitm=True).

## Selecting the attack model explicitly

Call `rot_primal_hybrid()` directly to select the attack model. There are three independent choices. Here, a **more conservative** setting gives the attacker more power and therefore gives a lower security estimate.

- **Close vector algorithm (`babai`)**: `babai=True` uses Babai's Nearest Plane algorithm. `babai=False` uses the stronger projected CVP model, so it is the more conservative choice.
- **Meet in the middle (`mitm`)**: `mitm=True` gives the attacker a search speedup.
- **MitM decomposition (`mitm_heuristic`)**: `estimator` charges `sqrt(poly_degree) * sqrt(search_space)`, corresponding to the decomposition already used by the Lattice Estimator. `square root` charges the lower `sqrt(search_space)`, corresponding to the isometric decomposition heuristic in the paper. `square root` is the more conservative of these two settings.

Taken together, `babai=False`, `mitm=True`, and `mitm_heuristic="square root"` give the most conservative setting accepted by the implementation. We do not include this combination in `estimate()`, or use it for our paper estimates, because the success probability of combining projected CVP with the MitM step has not been analysed. This follows the [Lattice Estimator `LWE.estimate()` function](https://github.com/malb/lattice-estimator/blob/6019056011d10d7e9c30a0d5da2d2f729fbc2eec/estimator/lwe.py#L142-L156), which likewise omits this combination as overly optimistic.

For example, these are the three Babai estimates used by `sparse_estimates.py` for the appendix table:

```python
from lwe_rot_primal import rot_primal_hybrid

ring_no_mitm_estimate = rot_primal_hybrid(
    params, babai=True, mitm=False, poly_degree=poly_degree
)

ring_estimator_mitm_estimate = rot_primal_hybrid(
    params,
    babai=True,
    mitm=True,
    mitm_heuristic="estimator",
    poly_degree=poly_degree,
)

ring_square_root_mitm_estimate = rot_primal_hybrid(
    params,
    babai=True,
    mitm=True,
    mitm_heuristic="square root",
    poly_degree=poly_degree,
)
```

## Estimating MLWE

For rank-`k` MLWE over a ring of degree `d`, set `params.n = k*d` and pass `poly_degree=d`. The default `poly_degree=params.n` is correct only for RLWE.

## Files

- `lwe_rot_primal.py` implements the estimator and the `estimate()` function.
- `lwe_rlwe_gap.py` generates the sparse LWE/RLWE gap estimates used in the paper.
- `sparse_gap.txt` contains the output of `lwe_rlwe_gap.py` used for the LWE/RLWE gap table.
- `sparse_estimates.py` estimates the recent sparse RLWE parameter sets in the appendix.
- `sparse_estimates.txt` contains the output of `sparse_estimates.py` used for the appendix table.
- `lattice_estimator/` is the pinned Lattice Estimator submodule used by this code.
