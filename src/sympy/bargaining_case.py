from sympy import Symbol, integrate, init_printing, simplify

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

simplify(pi_F.diff(N_P))
