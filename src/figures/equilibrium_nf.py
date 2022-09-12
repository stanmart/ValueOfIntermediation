import numpy as np
import matplotlib. pyplot as plt
import typer


def plot_equilibrium_nf(N_P_list, B, C, N_f_range, num_obs=500):
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


def create_plot(out_path: str, B: float = 1, C: float = 0.2,
                N_P: list[float] = [], N_f_range: tuple[float, float] = (0, 1),
                num_obs: int = 500, width: float = 5, height: float = 3.5, dpi: int = 300):

    if not N_P:
        raise typer.BadParameter("At least one value for N_P must be provided")

    fig, ax = plot_equilibrium_nf(N_P_list=N_P, B=B, C=C, N_f_range=N_f_range, num_obs=num_obs)

    fig.set_size_inches(width, height)
    fig.set_facecolor("white")

    fig.savefig(out_path, dpi=dpi)


if __name__ == "__main__":
    typer.run(create_plot)
