from sympy import Symbol, integrate, solve, Eq, init_printing, log, plot

init_printing()

x = Symbol('x')
N_F = Symbol('N_F')
f = x / (x + 1)

int_f_sN = integrate(f, (x, 0, N_F)) / N_F

int_1st = f.subs({x: N_F}) / N_F - int_f_sN / N_F
int_2nd = f.diff(x).subs({x: N_F}) / N_F - 2 * f.subs({x: N_F}) / N_F**2 + 2 * int_f_sN / N_F**2

eq_1 = Eq(f.diff(x).subs({x: N_F}), int_1st)
eq_2 = Eq(f.diff(x, 2).subs({x: N_F}), int_2nd)

plot(eq_1.lhs, eq_1.rhs, (N_F, 2, 5))
plot(eq_2.lhs, eq_2.rhs, (N_F, 2, 5))


sol_1 = solve(eq_1, log(1 + N_F))
sol_2 = solve(eq_2, log(1 + N_F))

plot(sol_1[0], sol_2[0], log(1+N_F), (N_F, 0, 5))

