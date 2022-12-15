from sympy import Symbol, init_printing, simplify, solve, Eq
from sympy import sqrt
import sympy.plotting as sp

init_printing()

mu = Symbol('mu')
V_F = Symbol('V_F')
V_P = Symbol('V_P')

I_F = Symbol('I_F')
F_F = Symbol('F_F')

N_F = Symbol('N_F')
N_P = Symbol('N_P')
n = Symbol('n')

A_eq = mu * V_F / (F_F + I_F)
A_def = N_F * V_F + N_P * V_P + 1

N_F_eq = simplify(solve(Eq(A_eq, A_def), N_F)[0])

pi_P = simplify(F_F * N_F_eq + N_P * mu * V_P / A_eq)

F_F_opt = simplify(solve(Eq(pi_P.diff(F_F), 0), F_F)[1])

pi_P_opt = simplify(pi_P.subs(F_F, F_F_opt))
pi_P_ret = mu * (N_P * V_P) / (N_P * V_P + 1)

N_P_bar = (sqrt(mu * V_F / I_F) - 1) / V_P

# Plotting
params_1 = {
    mu: 3,
    V_F: 1,
    V_P: 1,
    I_F: 0.5,
}
params_2 = {
    mu: 3,
    V_F: 1,
    V_P: 2,
    I_F: 0.5,
}

plot_single = sp.plot(
    pi_P_opt.subs(params_1),
    pi_P_ret.subs(params_1),
    (N_P, 0, 5),
    ylim=(0, 4),
    show=False
)
plot_single.append(
    sp.plot_implicit(Eq(N_P, N_P_bar.subs(params_1)), show=False)[0]
)
plot_single.show()

plot_multi = sp.plot(
    pi_P_opt.subs(params_1),
    pi_P_ret.subs(params_1),
    pi_P_opt.subs(params_2),
    pi_P_ret.subs(params_2),
    (N_P, 0, 5),
    ylim=(0, 4),
    show=False
)
plot_multi.append(
    sp.plot_implicit(Eq(N_P, N_P_bar.subs(params_1)), show=False)[0]
)
plot_multi.append(
    sp.plot_implicit(Eq(N_P, N_P_bar.subs(params_2)), show=False)[0]
)
plot_multi.show()

