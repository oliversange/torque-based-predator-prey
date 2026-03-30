import numpy as np


def WCA(x, y, number_of_particles, boundary_condition):
        
        x_m = np.tile(x, (number_of_particles, 1))
        y_m = np.tile(y, (number_of_particles, 1))

        # Calculate the differences in x and y coordinates
        dx = x_m - x_m.T
        dy = y_m - y_m.T

        # apply boundary condition
        if boundary_condition:
            dx = np.where(dx > 0.5 * 175, dx - 175, np.where(dx < -0.5 * 175, dx + 175, dx))
            dy = np.where(dy > 0.5 * 175, dy - 175, np.where(dy < -0.5 * 175, dy + 175, dy))

        r_ij = np.sqrt(dx**2 + dy**2)

        #fill diagonals
        np.fill_diagonal(r_ij, np.inf)
        np.fill_diagonal(dx, 0)
        np.fill_diagonal(dy, 0)

        force_x_i = -1 * np.sum(np.where(r_ij < 2**(1/6), 1.0, 0.0) * dx * 4800 * (1 / r_ij ** 14 - 0.5 * 1 / r_ij ** 8), axis=1)
        force_y_i = -1 * np.sum(np.where(r_ij < 2**(1/6), 1.0, 0.0) * dy * 4800 * (1 / r_ij ** 14 - 0.5 * 1 / r_ij ** 8), axis=1)

        return [force_x_i, force_y_i]