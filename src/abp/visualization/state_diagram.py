import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def plot_state_diagram():

    # Visuals
    mpl.rcParams['xtick.labelsize'] = 13
    mpl.rcParams['ytick.labelsize'] = 13

    cmap = plt.cm.viridis
    fontsize = 14
    marker_size = 150

    # Data
    shape_dict = {
        0.1: ['h', 'h', 'h', 'h'],
        1:   ['h', 'h', 'p', 'p'],
        10:  ['p', 's', '^', '^'],
        20:  ['p', 's', '^', '^'],
        30:  ['p', '^', '^', '^'],
        40:  ['p', '^', '^', '^']
    }

    color_map = {
        'h': cmap(0.8),
        'p': cmap(0.6),
        's': cmap(0.4),
        '^': cmap(0.2)
    }

    labels_added = {
        'h': False,
        'p': False,
        's': False,
        '^': False
    }

    label_text = {
        '^': 'one group',
        's': 'multiple cohesive groups',
        'p': 'multiple loose groups',
        'h': 'cloud'
    }

    # Plotting
    fig, ax = plt.subplots()

    for torque, shapes in shape_dict.items():
        for i, shape in enumerate(shapes):
            y = i + 2

            # Add legend entries only once per shape
            if not labels_added[shape]:
                ax.scatter(
                    torque, y,
                    c=color_map[shape],
                    marker=shape,
                    s=marker_size,
                    label=label_text[shape]
                )
                labels_added[shape] = True

            # Main scatter points
            ax.scatter(
                torque, y,
                c=color_map[shape],
                marker=shape,
                s=marker_size
            )

    # Separation lines
    ax.plot([0.4, 0.4, 4, 4], [6, 3.5, 3.5, 1], c=cmap(0.8))
    ax.plot([4, 4, 40], [6, 2.5, 2.5], c=cmap(0.6))
    ax.plot([4, 4, 25, 25, 60], [5, 3.5, 3.5, 2.5, 2.5], c=cmap(0.4))

    # Formatting
    ax.set_xscale('log')

    ax.set_xlabel(r'prey-prey interaction torque $T_{\mathrm{A}}$', fontsize=fontsize)
    ax.set_ylabel(r'prey-prey interaction radius $R_{\mathrm{pp}}$ in $r_{\mathrm{c}}$', fontsize=fontsize)

    ax.set_xlim(0.08, 50)
    ax.set_ylim(1.8, 5.2)

    ax.legend(
        loc='upper center',
        fontsize=fontsize,
        bbox_to_anchor=(0.5, 1.25),
        ncol=2
    )

    fig.subplots_adjust(top=0.85)

    return fig, ax