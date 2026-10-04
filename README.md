  # On the Concrete Hardness Gap Between MLWE and LWE

  This repository contains the estimation and simulation code accompanying
  [*On the Concrete Hardness Gap Between MLWE and LWE*](https://eprint.iacr.org/2026/279).

  ## Repository structure

  - [`PrimalHybrid/`](PrimalHybrid/) contains our estimator for the primal hybrid
    attack with rotations, together with the scripts used for the sparse-secret
    estimates in the paper. See the
    [PrimalHybrid README](PrimalHybrid/README.md) for setup, examples, and a
    discussion of the available attack models.

  - [`DualHybrid/`](DualHybrid/) contains the code used for the dual hybrid
    estimates for Kyber. It is a submodule based on the original
    [CodedDualAttack repository](https://github.com/kevin-carrier/CodedDualAttack).
    Our changes are contained in `DualHybrid/OptimizeCodedDualAttack/`.

  - [`simulations/`](simulations/) contains the probability simulations used in
    the paper.

  ## Setup

  Clone the repository and its submodules with

  ```bash
  git clone --recurse-submodules https://github.com/TabOg/mlwe-hybrids.git

  or initialise the submodules after cloning:

  git submodule update --init --recursive

  ## Primal hybrid estimates

  See the PrimalHybrid README (PrimalHybrid/README.md).

  ## Dual hybrid estimates

  The main files in DualHybrid/OptimizeCodedDualAttack/ are:

  - optimizer_naive.py, which runs the parameter search;
  - utilitaries.py, which implements the cost calculation;
  - mlwe_*.pkl and lwe_*.pkl, containing the initial, intermediate, and final
    optimization results;

  - mlwe_results_full.txt and lwe_results_full.txt, containing the complete
    final results used in the paper;

  - read_final_results.py, which converts the final .pkl files into readable
    output.

  After activating SageMath, run:

  cd DualHybrid/OptimizeCodedDualAttack
  make
  python3 optimizer_naive.py

  The full optimization takes several hours.