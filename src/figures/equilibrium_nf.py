import numpy as np
import matplotlib. pyplot as plt


def plot_equilibrium_nf(N_P_list, B, C, N_f_range=(0, 2), num_obs=500):
    N_f = np.linspace(N_f_range[0], N_f_range[1], num_obs)
    rhs = C * N_f
    lhs_list = []
    for N_P in N_P_list:
        lhs = (np.log(B * N_P + B * N_f + 1) - np.log(B * N_P + 1)) / (B * N_f) - 1 / (N_P * B + N_f * B + 1)
        lhs_list.append(lhs)

    fig, ax = plt.subplots()
    ax.plot(N_f, rhs, label=r'$C\barN_f$', color='black')
    for lhs, N_P in zip(lhs_list, N_P_list):
        ax.plot(N_f, lhs, label=r'$h(\bar N_f) \mid N_P = {}$'.format(N_P))

    ax.set_xlabel(r'$\barN_f$')
    ax.legend()

    return fig, ax


fig, ax = plot_equilibrium_nf([0, 0.2], B=1, C=0.2, N_f_range=(0, 1))
fig.set_size_inches(5, 3.5)
fig.set_facecolor("white")
fig.savefig("../../out/figures/equilibrium_nf.png", dpi=300)