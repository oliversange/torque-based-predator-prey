import numpy as np

def det_T(x, y, theta, pred_x, pred_y, pred_theta, number_of_particles, boundary_condition, T_A, T_0, R_prey, R_prey_pred):

        # Determine the Prey-Prey-Term
        x_m = np.tile(x, (number_of_particles, 1))
        y_m = np.tile(y, (number_of_particles, 1))
        theta_matrix = np.tile(theta, (number_of_particles, 1))

        # Calculate distance in x and y coordinates
        dx = x_m - x_m.T
        dy = y_m - y_m.T
        delta_theta = theta_matrix - theta_matrix.T

        #apply boundary condition
        if boundary_condition:
            dx = np.where(dx > 0.5 * 175, dx - 175, np.where(dx < -0.5 * 175, dx + 175, dx))
            dy = np.where(dy > 0.5 * 175, dy - 175, np.where(dy < -0.5 * 175, dy + 175, dy))

        # Calculate the distances between particles
        distances = np.sqrt(dx**2 + dy**2)

        # Exclude the diagonal elements (i == j)
        np.fill_diagonal(distances, np.inf)

        u = np.column_stack((np.cos(theta), np.sin(theta)))
        u_n = u / np.linalg.norm(u)
        cp = (u_n[:, 0, np.newaxis] * dy - u_n[:, 1, np.newaxis] * dx) / distances

        # Calculate the Prey-Prey-Term
        prey_term = T_A * np.sum(np.where((R_prey - distances) > 0, 1, 0) * (np.sin(delta_theta) + 0.5 * cp), axis=1)

        # calculate Predator-Prey distances in x and y coordinates
        distance_pred_particle_x = x - pred_x
        distance_pred_particle_y = y - pred_y

        # apply boundary condition
        if boundary_condition:
            distance_pred_particle_x = np.where(distance_pred_particle_x > 0.5 * 175, distance_pred_particle_x - 175, np.where(distance_pred_particle_x < -0.5 * 175, distance_pred_particle_x + 175, distance_pred_particle_x))
            distance_pred_particle_y = np.where(distance_pred_particle_y > 0.5 * 175, distance_pred_particle_y - 175, np.where(distance_pred_particle_y < -0.5 * 175, distance_pred_particle_y + 175, distance_pred_particle_y))

        #calculate distance
        pred_distance = np.sqrt(distance_pred_particle_x**2 + distance_pred_particle_y**2)

        pred_cp = np.cos(pred_theta) * distance_pred_particle_y - np.sin(pred_theta) * distance_pred_particle_x

        # Calculate the Predator-Prey-Term
        predator_term = T_0 * np.where((R_prey_pred - pred_distance) > 0, 1, 0) * (pred_cp / pred_distance)

        T = prey_term + predator_term
        return T

def det_pred_T(x, y, pred_x, pred_y, pred_theta, T_0_predator, R_pred_prey, boundary_condition):

        # Calculate distance in x and y coordinates
        pred_prey_x = x - pred_x
        pred_prey_y = y - pred_y
        if boundary_condition:
            pred_prey_x = np.where(pred_prey_x > 0.5 * 175, pred_prey_x - 175, np.where(pred_prey_x < -0.5 * 175, pred_prey_x + 175, pred_prey_x))
            pred_prey_y = np.where(pred_prey_y > 0.5 * 175, pred_prey_y - 175, np.where(pred_prey_y < -0.5 * 175, pred_prey_y + 175, pred_prey_y))

        # Calculate distance
        pred_prey_x_y = np.sqrt(pred_prey_x**2 + pred_prey_y**2)

        # Eating mechanism
        bed = pred_prey_x_y < 1.0
        eating_count = np.sum(bed)
        x[bed] += 1000000000000

        # Calculate cross product components
        pred_cp = np.cos(pred_theta) * pred_prey_y - np.sin(pred_theta) * pred_prey_x

        # Calculate T_P_j
        T_P_j = T_0_predator * np.sum(np.where(pred_prey_x_y < R_pred_prey, 1.0, 0.0) * (pred_cp / pred_prey_x_y))

        return T_P_j, x, eating_count