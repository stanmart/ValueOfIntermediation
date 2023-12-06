import pandas as pd
import numpy as np
from scipy.optimize import fsolve
from collections.abc import Iterable
import typer
from sympy import Symbol, integrate, simplify, log, lambdify


def create_plot_data(
    out_path: str,
    mu: float = 1,
    V_P: float = 1,
    V_F: float = 1,
    I_F: float = 0.2,
    N_P_range: tuple[float, float] = (0, 1),
    num_obs: int = 500,
    value_function: str = "profit",
    bargaining: str = "one-sided",
):
    
    N_P_sp, N_F_sp = Symbol("N_P"), Symbol("N_F")
    s = Symbol("s")

    f_profit = mu * (s * N_F_sp * V_F + N_P_sp * V_P) / (s * N_F_sp * V_F + N_P_sp * V_P + 1)
    f_surplus = mu * log(s * N_F_sp * V_F + N_P_sp * V_P + 1)

    if value_function == "profit":
        f = f_profit
    elif value_function == "welfare":
        f = f_profit + f_surplus
    else:
        raise typer.BadParameter(f"Unknown value function: {value_function}")
    
    if bargaining == "onesided":
        pi_P_symbolic = simplify(integrate(f, (s, 0, 1)))
        pi_F_symbolic = simplify(integrate(s * f.diff(s), (s, 0, 1)))
    elif bargaining == "twosided":
        pi_P_symbolic = simplify(integrate(s * f, (s, 0, 1)))
        pi_F_symbolic = simplify(integrate(s**2 * f.diff(s), (s, 0, 1)))
    else:
        raise typer.BadParameter(f"Unknown bargaining mode: {bargaining}")
    
    pi_P = lambdify((N_P_sp, N_F_sp), pi_P_symbolic)
    pi_F = lambdify((N_P_sp, N_F_sp), pi_F_symbolic)

    def pi_F_t(N_P, N_F):
        return pi_F(N_P, N_F) - I_F * N_F

    def N_F_opt(N_P):
        if isinstance(N_P, Iterable):
            return np.array([N_F_opt(n) for n in N_P])
        else:
            return fsolve(lambda N_F: pi_F_t(N_P, N_F), 3)[0]

    N_P_vec = np.linspace(N_P_range[0], N_P_range[1], num_obs)
    N_F_vec = N_F_opt(N_P_vec)

    pi_F_vec = pi_F(N_P_vec, N_F_vec)
    pi_P_vec = pi_P(N_P_vec, N_F_vec)
    A_vec = N_P_vec * V_P + N_F_vec * V_F + 1
    CS_vec = np.log(A_vec)

    N_F_cf = np.maximum(N_F_vec[0] * V_F - N_P_vec * V_P, 0)
    A_cf = N_P_vec * V_P + N_F_cf * V_F + 1
    CS_cf = np.log(A_cf)

    A_noF = N_P_vec * V_P + 1
    CS_noF = np.log(A_noF)
    pi_P_noF = mu * N_P_vec * V_P / A_noF

    pi_P_var_vec = mu * N_P_vec * V_P / A_vec
    F_F_implied = np.where(
        N_F_vec > 1e-5,
        (pi_P_vec - pi_P_var_vec) / N_F_vec,
        np.nan
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
            "A_noF": A_noF,
            "CS_noF": CS_noF,
            "pi_P_noF": pi_P_noF,
            "F_F_implied": F_F_implied,
        }
    )

    data.to_csv(out_path, index=False)


if __name__ == "__main__":
    typer.run(create_plot_data)
