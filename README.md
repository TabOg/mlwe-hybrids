# On the Concrete Hardness Gap Between MLWE and LWE

This repository contains the estimation and simulation code accompanying [*On the Concrete Hardness Gap Between MLWE and LWE*](https://eprint.iacr.org/2026/279).

## Repository structure

- [`PrimalHybrid/`](https://github.com/TabOg/mlwe-hybrids/tree/master/PrimalHybrid) contains our estimator for the primal hybrid attack with rotations, together with the scripts used for the sparse secret estimates in the paper. See the [Primal Hybrid README](https://github.com/TabOg/mlwe-hybrids/blob/master/PrimalHybrid/README.md) for setup, examples, and a discussion of the available attack models.
- [`DualHybrid/`](https://github.com/TabOg/CodedDualAttack) contains the code used for the dual hybrid estimates for Kyber. It is a submodule based on the original [CodedDualAttack repository](https://github.com/kevin-carrier/CodedDualAttack). Our changes are contained in `OptimizeCodedDualAttack/`.
- [`simulations/`](https://github.com/TabOg/mlwe-hybrids/tree/master/simulations) contains the probability simulations used in the paper.

## Setup

Clone the repository and its submodules with:

```bash
git clone --recurse-submodules https://github.com/TabOg/mlwe-hybrids.git
cd mlwe-hybrids
```

For an existing clone, initialise or update the submodules with:

```bash
git submodule update --init --recursive
```

## Primal Hybrid Estimates

See the [Primal Hybrid README](https://github.com/TabOg/mlwe-hybrids/blob/master/PrimalHybrid/README.md).

## Dual Hybrid Estimates

The main files in `DualHybrid/OptimizeCodedDualAttack/` are:

- `optimizer_naive.py`, which runs the parameter search;
- `utilitaries.py`, which implements the cost calculation;
- `mlwe_*.pkl` and `lwe_*.pkl`, containing the initial, intermediate, and final optimisation results;
- `mlwe_results_full.txt` and `lwe_results_full.txt`, containing the complete final results used in the paper;
- `read_final_results.py`, which converts the final `.pkl` files into readable output.

After activating SageMath, run:

```bash
cd DualHybrid/OptimizeCodedDualAttack
make
python3 optimizer_naive.py
```

The full optimisation takes several hours.
