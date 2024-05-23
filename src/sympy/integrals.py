from sympy import Eq, Symbol, init_printing, integrate, simplify, solve

init_printing()

mu = Symbol("mu")
B = Symbol("B")
C = Symbol("C")
Nf = Symbol("N_f")
Np = Symbol("N_P")
Nfbar = Symbol("\\bar N_f")

v = (Np * B + Nf * B) / (Np * B + Nf * B + 1)

P_share = simplify(integrate(v, (Nf, 0, Nfbar)) / Nfbar)
F_share = simplify(v.subs({Nf: Nfbar}) - P_share)

Nfbar_eq = Eq(Nfbar * C, F_share)
Nfbar_opt = solve(Nfbar_eq, Nfbar)
