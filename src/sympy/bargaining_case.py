from sympy import (
    Symbol,
    init_printing,
    integrate,
    log,  # type: ignore
    plot,
    simplify,
)

init_printing()

mu = Symbol("mu")
V_F = Symbol("V_F")
V_P = Symbol("V_P")

I_F = Symbol("I_F")

N_F = Symbol("N_F")
N_P = Symbol("N_P")
n = Symbol("n")

v = mu * (n * V_F + N_P * V_P) / (n * V_F + N_P * V_P + 1)

pi_P = simplify(integrate(v, (n, 0, N_F)) / N_F)
pi_F = simplify(v.subs({n: N_F}) - pi_P)

pi_P
pi_F

pi_F_t = pi_F - I_F * N_F
# solve(pi_F_t, N_F)  # :(

pi_F_alt = mu * (
    log(1 + (N_F * V_F) / (N_P * V_P + 1)) / (N_F * V_F)
    - 1 / (N_P * V_P + N_F * V_F + 1)
)
pi_F_t_alt = pi_F_alt - I_F * N_F
d_N_F_N_P = simplify(pi_F_t_alt.diff(N_F) / pi_F_t_alt.diff(N_P))

simplify((pi_F_alt).diff(N_F))
simplify((pi_F_alt).diff(N_F).diff(N_F))
simplify((pi_F_alt).diff(N_F).diff(N_F).diff(N_F))

(2 * log((N_F * V_F) / (N_P * V_P + 1) + 1)).diff(N_F)  # type: ignore

plot_params = {V_F: 1, N_P: 0.5, V_P: 1, mu: 1}
plot(
    pi_F_alt.subs(plot_params),
    (N_F, 0, 10),
)
plot(
    simplify((pi_F_alt).diff(N_F)).subs(plot_params),
    simplify((pi_F_alt).diff(N_F).diff(N_F)).subs(plot_params),
    (N_F, 3, 5),
)

# unfortunately the result of this has an ambiguous sign:
simplify(
    simplify(
        (pi_F_alt).diff(N_F).diff(N_F) * N_F**3 * V_F * (N_F * V_F + N_P * V_P + 1) ** 3
    )
    + simplify(
        2 * (pi_F_alt).diff(N_F) * N_F**2 * V_F * (N_F * V_F + N_P * V_P + 1) ** 3
    )
)

simplify(
    simplify(
        (pi_F_alt).diff(N_F).diff(N_F) * N_F**3 * V_F * (N_F * V_F + N_P * V_P + 1) ** 3
    )
    + simplify(
        2
        * (pi_F_alt).diff(N_F)
        * N_F**2
        * V_F
        * (N_F * V_F + N_P * V_P + 1) ** 2
        * N_F
        * V_F
    )
)
