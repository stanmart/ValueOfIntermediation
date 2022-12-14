from sympy import Symbol, init_printing, simplify, solve, Eq

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
