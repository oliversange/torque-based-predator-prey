import numpy as np
import matplotlib.pyplot as plt

# WCA potential
def wca(r):
    result = np.where(r <= 2**(1/6), 4 * 100* ((1/r)**12 - (1/r)**6) + 100, 0)
    return result

def plot_wca_potential(r, x, y, x_1, y_1, wca=wca, fontsize=14):

    cmap = plt.get_cmap("inferno")

    fig, ax = plt.subplots()

    ax.plot(r, wca(r), c=cmap(0.2), label=r"WCA potential $U_{100, 1}$")
    ax.plot(x, y, c=cmap(0.4), linewidth=0.8, linestyle="--",
            label=r"cutoff radius $r_c$")
    ax.plot(x_1, y_1, c=cmap(0.5), linewidth=0.8, linestyle=":",
            label=r"particle diameter $\sigma$")

    ax.set_ylim(0, 100)
    ax.set_xlim(0.9, 1.3)

    ax.set_xlabel(r"distance between particles $r$", fontsize=fontsize)
    ax.set_ylabel(r"WCA potential $U_{\epsilon, \sigma}$", fontsize=fontsize)

    ax.grid()
    ax.legend(fontsize=fontsize)

    return fig, ax
