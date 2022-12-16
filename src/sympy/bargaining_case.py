from sympy import Symbol, integrate, init_printing, simplify, factor, solve

init_printing()

mu = Symbol('mu')
V_F = Symbol('V_F')
V_P = Symbol('V_P')

I_F = Symbol('I_F')

N_F = Symbol('N_f')
N_P = Symbol('N_P')
n = Symbol('n')

v = mu * (n * V_F + N_P * V_P) / (n * V_F + N_P * V_P + 1)

pi_P = simplify(integrate(v, (n, 0, N_F)) / N_F)
pi_F = simplify(v.subs({n: N_F}) - pi_P)

pi_P
pi_F

pi_F_t = pi_F - I_F * N_F
solve(pi_F_t, N_F)  # :(

d_N_F = simplify(pi_F_t.diff(N_F))
d_N_P = simplify(pi_F_t.diff(N_P))

d_N_F_N_P = factor(simplify(d_N_F / d_N_P))
d_N_F_N_P

pi_F_simplified = mu * (
    (N_P * V_P + N_F * V_F) / (N_P * V_P + N_F * V_F + 1)
    - 1
    - 1 / (N_F * V_F)
) - I_F * N_F
d_N_F_N_P_simplified = simplify(
    pi_F_simplified.diff(N_F) / pi_F_simplified.diff(N_P)
)
