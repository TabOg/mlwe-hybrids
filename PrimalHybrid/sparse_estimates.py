from multiprocessing import cpu_count

import sage
from lattice_estimator.estimator import *
from sage.all import oo
from lwe_rot_primal import rot_primal_hybrid
from lwe_rot_primal import estimate as rot_primal_estimate

# log n, log q, h, sigma
sparse_params = [
    (13, 55, 31, 3.2), # SHIP -- EC25
    (14, 100, 31, 3.2), # SHIP -- EC25
    (15, 105, 31, 3.2), # SHIP -- EC25
    (11, 52, 256, 3.2), # CCMULT -- EC25
    (12, 64, 256, 3.2), # CCMULT -- EC25
    (12, 104, 256, 3.2), # CCMULT -- EC25
    (13, 117, 256, 3.2), # CCMULT -- EC25
    (13, 178, 256, 3.2), # CCMULT -- EC25
    (14, 420, 256, 3.2), # GBFV -- EC25
    (14, 120, 32, 3.2), # GBFV -- EC25
    (15, 767, 192, 3.19), # GFB -- C25
    (16, 1553, 192, 3.19), # GFB -- C25
    (17, 3104, 192, 3.19), # GFB -- C25
    (16, 1518, 192, 3.2), # RNS -- C25
    (16, 104, 32, 3.2), # RNS -- C25
    (15, 679, 192, 3.2), # GRAFT -- CCS25
    (15, 780, 192, 3.2), # GRAFT -- CCS25
    (16, 1555, 192, 3.2), # GRAFT -- CCS25
    (16, 1533, 192, 3.2), # Discrete -- CCS25
    (16, 118, 30, 3.2), # Discrete -- CCS25
    (16, 300, 128, 3.2), # THOR -- CCS25
    (11, 64, 35, 2 ** 49), # TFHE -- CCS25   
    (11, 64, 38, 2 ** 47), # TFHE -- CCS25
    (12, 64, 30, 2 ** 43), # TFHE -- CCS25
    (13, 64, 25, 2 ** 43), # TFHE -- CCS25
    (12, 64, 32, 2 ** 40), # TFHE -- CCS25
    (13, 64, 26, 2 ** 41), # TFHE -- CCS25
    (15, 934, 64, 3.2), # PACO -- CCS25
    (16, 1496, 64, 3.2), # PACO -- CCS25
]

def print_dict(d):
    print("{")
    for k, v in d.items():
        print(f"\t{k}:\t\t\t{v!r}")
    print("}")

cost_model = RC.MATZOV
for (logn, logq, h, sigma) in sparse_params:
    if sigma < 10:
        print(f"{logn=} {logq=} {h=} {sigma=}")
    else:
        log_sigma = sage.all.log(sigma, 2) // 1
        print(f"{logn=} {logq=} {h=} {log_sigma=}")
    h_half = h // 2
    h_half_ = h - h_half
    params = LWE.Parameters(n=2**logn, q = 2**logq, Xs=ND.SparseTernary(p=h_half, m=h_half_, n=2 ** logn), Xe=ND.DiscreteGaussian(stddev=sigma))

    # run all estimating scripts apart from "arora-gb", which is not relevant for sparse secrets and doesn't terminate for large values of n
    if logn < 14:
        lwe_estimates = LWE.estimate(params, quiet=True, jobs=cpu_count() // 4, deny_list=["arora-gb"])
        
    # estimator doesn't terminate for large values: just run the two best performing attacks (dual hybrid, bdd mitm hybrid)
    else:
        plain_primal_hybrid_estimate = LWE.primal_hybrid(params, babai=True, mitm=True)
        plain_dual_hybrid_estimate = LWE.dual_hybrid(params)
        lwe_estimates={'bdd_mitm_hybrid': plain_primal_hybrid_estimate, 'dual_hybrid': plain_dual_hybrid_estimate}

    print("plain lwe estimates:")
    print_dict(lwe_estimates)
    print()

    # these are all RLWE; poly_degree = params.n
    poly_degree = params.n
    rlwe_estimates = rot_primal_estimate(params, poly_degree=poly_degree)
    print("rlwe estimates:")
    print_dict(rlwe_estimates)
    print()

    # this corresponds to heuristic 1 in the paper, i.e., only a square root split of the plain set is possible.
    # we call this "estimator" because this is the same heuristic used by the lattice estimator.
    # we omit this estimate as it is less conservative than the "square root" heuristic
    # mitm_cost = rot_primal_hybrid(params, babai=True, mitm=True, poly_degree=poly_degree, mitm_heuristic="estimator")
    # print(f"\testimator {mitm_cost=}")
    # print()
    
sparse_params_ternary_error = [
    (14, 404, 256) # AC25
]

for (logn, logq, h) in sparse_params_ternary_error:
    print(f"{logn=} {logq=} {h=} ternary_error")
    h_half = h // 2
    h_half_ = h - h_half
    params = LWE.Parameters(n=2**logn, q = 2**logq, Xs=ND.SparseTernary(p=h_half, m=h_half_, n=2 ** logn), Xe=ND.Uniform(-1, 1))

    # run all estimating scripts apart from "arora-gb", which is not relevant for sparse secrets and doesn't terminate for large values of n
    if logn < 14:
        lwe_estimates = LWE.estimate(params, quiet=True, jobs=cpu_count() // 4, deny_list=["arora-gb"])
        
    # estimator doesn't terminate for large values: just run the two best performing attacks (dual hybrid, bdd mitm hybrid)
    else:
        plain_primal_hybrid_estimate = LWE.primal_hybrid(params, babai=True, mitm=True)
        plain_dual_hybrid_estimate = LWE.dual_hybrid(params)
        lwe_estimates={'bdd_mitm_hybrid': plain_primal_hybrid_estimate, 'dual_hybrid': plain_dual_hybrid_estimate}

    print("plain lwe estimates:")
    print_dict(lwe_estimates)
    print()

    # these are all RLWE; poly_degree = params.n
    poly_degree = params.n
    rlwe_estimates = rot_primal_estimate(params, poly_degree=poly_degree)
    print("rlwe estimates:")
    print_dict(rlwe_estimates)
    print()

    # this corresponds to heuristic 1 in the paper, i.e., only a square root split of the plain set is possible.
    # we call this "estimator" because this is the same heuristic used by the lattice estimator.
    # we omit this estimate as it is less conservative than the "square root" heuristic
    # mitm_cost = rot_primal_hybrid(params, babai=True, mitm=True, poly_degree=poly_degree, mitm_heuristic="estimator")
    # print(f"\testimator {mitm_cost=}")
    # print()


    