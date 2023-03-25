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

    N_P_vec = np.linspace(N_P_range[0], N_P_range[1], num_obs)
    N_F_vec = N_F_opt(N_P_vec)
    N_F_cf_vec = np.maximum(N_F_vec[0] * V_F - N_P_vec * V_P, 0)

    pi_F_vec = pi_F(N_P_vec, N_F_vec)
    pi_P_vec = pi_P(N_P_vec, N_F_vec)
    A_vec = N_P_vec * V_P + N_F_vec * V_F + 1
    CS_vec = np.log(A_vec)

    data = pd.DataFrame(
        {
            "N_P": N_P_vec,
            "N_F": N_F_vec,
            "pi_F": pi_F_vec,
            "pi_P": pi_P_vec,
            "A": A_vec,
            "CS": CS_vec,
            "N_F_cf": N_F_cf_vec,
        }
    )

    data.to_csv(out_path, index=False)


if __name__ == "__main__":
    typer.run(create_plot_data)
