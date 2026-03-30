import numpy as np
from tqdm import tqdm

def calc_prox_metrics(positions, R, boundary_condition, L, number_of_steps):
     
    x_positions = positions[0]
    y_positions = positions[1]

    particles_in_prox_cum = 0
    particle_distance_cum = 0

    for i, x in enumerate(tqdm(x_positions, total=len(x_positions), desc="Computing proximity metrics")):

        y = y_positions[i]
        eaten_particles_mask = x < 1000
        x_masked = x[eaten_particles_mask]
        y_masked = y[eaten_particles_mask]
        prey_size = np.size(x_masked)

        x_m = np.tile(x_masked, (prey_size, 1))
        y_m = np.tile(y_masked, (prey_size, 1))

        # Calculate the differences in x and y coordinates
        dx = x_m - x_m.T
        dy = y_m - y_m.T

        # apply boundary condition
        if boundary_condition:
            dx_bc = np.where(dx > 0.5 * L, dx - L, np.where(dx < -0.5 * L, dx + L, dx))
            dy_bc = np.where(dy > 0.5 * L, dy - L, np.where(dy < -0.5 * L, dy + L, dy))

        r_ij = np.sqrt(dx_bc**2 + dy_bc**2)

        # fill diagonals
        np.fill_diagonal(r_ij, 0)

        # Calculate the average distance
        sum_distances = np.sum(r_ij)
        num_distances = prey_size * (prey_size - 1)  # Number of unique off-diagonal elements

        particle_distance = sum_distances / num_distances

        # Calculate the average number of particles within distance R
        neighbor_counts = np.sum(r_ij < R, axis=1)  # Count neighbors within distance R for each particle
        particles_in_prox = np.mean(neighbor_counts) - 1  # Subtract 1 to exclude self

        particles_in_prox_cum += particles_in_prox
        particle_distance_cum += particle_distance

    av_particles_in_prox = particles_in_prox_cum / (number_of_steps/1000)
    av_particle_distance = particle_distance_cum / (number_of_steps/1000)

    return av_particles_in_prox, av_particle_distance
    