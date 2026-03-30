import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_simulation(
    positions,
    predator_positions,
    box_size,
    interval=50,
):
    """
    Animate predator-prey simulation.

    Expected input shapes:
        positions: (2, T, N)
        predator_positions: (2, T, 1)
    """

    positions = np.asarray(positions)
    predator_positions = np.asarray(predator_positions)

    # Extract dimensions
    _, T, N = positions.shape

    fig, ax = plt.subplots()

    # Initial frame
    prey_scatter = ax.scatter(
        positions[0, 0, :],  # x at t=0
        positions[1, 0, :],  # y at t=0
        s=20,
        label="Prey"
    )

    predator_scatter = ax.scatter(
        predator_positions[0, 0, 0],  # x at t=0
        predator_positions[1, 0, 0],  # y at t=0
        s=80,
        label="Predator"
    )

    # Static plot settings
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    ax.set_aspect("equal")
    ax.set_xlabel(r"x coordinates in units of $\sigma$")
    ax.set_ylabel(r"y coordinates in units of $\sigma$")
    ax.legend()

    def update(frame):
        # Prey: shape (N, 2)
        prey_xy = np.column_stack((
            positions[0, frame, :],
            positions[1, frame, :]
        ))

        prey_scatter.set_offsets(prey_xy)

        # Predator: shape (1, 2)
        predator_xy = np.array([[
            predator_positions[0, frame, 0],
            predator_positions[1, frame, 0]
        ]])

        predator_scatter.set_offsets(predator_xy)

        return prey_scatter, predator_scatter

    ani = FuncAnimation(
        fig,
        update,
        frames=T,
        interval=interval,
        blit=True
    )

    plt.show()

    return ani