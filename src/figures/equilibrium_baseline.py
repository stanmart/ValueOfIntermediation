import pandas as pd
import numpy as np
from scipy.optimize import fsolve
from collections.abc import Iterable
import typer


def create_plot_data(
    out_path: str,
    mu: float = 1,
    V_P: float = 1,
    V_F: float = 1,
    I_F: float = 0.2,
    N_P_range: tuple[float, float] = (0, 1),
    num_obs: int = 500,
):
    def f(N_P, N_F):
        return mu * (N_F * V_F + N_P * V_P) / (N_F * V_F + N_P * V_P + 1)

    def pi_P(N_P, N_F):
        inner_part = np.log(1 + (N_F * V_F) / (N_P * V_P + 1)) / (N_F * V_F)
        return mu * (1 - inner_part)

    def pi_F(N_P, N_F):
        first_part = np.log(1 + (N_F * V_F) / (N_P * V_P + 1)) / (N_F * V_F)
        second_part = 1 / (N_P * V_P + N_F * V_F + 1)
        return mu * (first_part - second_part)

    def pi_F_t(N_P, N_F):
        return pi_F(N_P, N_F) - I_F * N_F

    def N_F_opt(N_P):
        if isinstance(N_P, Iterable):
            return np.array([N_F_opt(n) for n in N_P])
        else:
            return fsolve(lambda N_F: pi_F_t(N_P, N_F), 1)[0]
        
    def F_F_opt():
        return np.sqrt(mu * I_F * V_F) - I_F
        
    def N_F_opt_bench(N_P):
        F_F = F_F_opt()
        N_F_candidate = mu / (F_F + I_F) - N_P * V_P / V_F - 1 / V_F
        return np.maximum(N_F_candidate, 0)

    N_P_vec = np.linspace(N_P_range[0], N_P_range[1], num_obs)
    N_F_vec = N_F_opt(N_P_vec)

    pi_F_vec = pi_F(N_P_vec, N_F_vec)
    pi_P_vec = pi_P(N_P_vec, N_F_vec)
    A_vec = N_P_vec * V_P + N_F_vec * V_F + 1
    CS_vec = np.log(A_vec)

    N_F_cf = np.maximum(N_F_vec[0] * V_F - N_P_vec * V_P, 0)
    A_cf = N_P_vec * V_P + N_F_cf * V_F + 1
    CS_cf = np.log(A_cf)

    N_F_bench = N_F_opt_bench(N_P_vec)
    A_bench = N_P_vec * V_P + N_F_bench * V_F + 1
    CS_bench = np.log(A_bench)
    pi_P_bench = F_F_opt() * N_F_bench + mu * N_P_vec * V_P / A_bench

    A_noF = N_P_vec * V_P + 1
    CS_noF = np.log(A_noF)
    pi_P_noF = mu * N_P_vec * V_P / A_noF

    pi_P_var_vec = mu * N_P_vec * V_P / A_vec
    F_F_opt_vec = np.where(
        N_F_bench > 1e-5,
        F_F_opt(),
        np.nan
    )
    F_F_implied = np.where(
        N_F_vec > 1e-5,
        (pi_P_vec - pi_P_var_vec) / N_F_vec,
        np.nan
    )

    hybrid = np.where(
        N_F_vec > 1e-5,
        10,
        0
    )

    hybrid_bench = np.where(
        N_F_bench_vec > 1e-5,
        10,
        0
    )


    data = pd.DataFrame(
        {
            "N_P": N_P_vec,
            "N_F": N_F_vec,
            "pi_F": pi_F_vec,
            "pi_P": pi_P_vec,
            "A": A_vec,
            "CS": CS_vec,
            "N_F_cf": N_F_cf,
            "A_cf": A_cf,
            "CS_cf": CS_cf,
            "N_F_bench": N_F_bench,
            "A_bench": A_bench,
            "CS_bench": CS_bench,
            "pi_P_bench": pi_P_bench,
            "A_noF": A_noF,
            "CS_noF": CS_noF,
            "pi_P_noF": pi_P_noF,
            "F_F_implied": F_F_implied,
            "F_F_opt": F_F_opt_vec,
        }
    )

    data.to_csv(out_path, index=False)


if __name__ == "__main__":
    typer.run(create_plot_data)
