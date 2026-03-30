import numpy as np
from tqdm import tqdm
from src.abp.starting_parameters.prey_starting_parameters import calculate_prey_starting_parameters
from src.abp.starting_parameters.predator_starting_parameters import *
from src.abp.forces.wca import WCA
from src.abp.forces.torques import *

def simulate(number_of_particles,
               number_of_steps,
               predator_introduction_step,
               setup,
               dt, 
               v0, 
               v_pred, 
               D, 
               D_rot, 
               mu, 
               mu_r, 
               T_A, 
               T_0, 
               T_0_predator,
               R_prey, 
               R_prey_pred,
               R_pred_prey,
               boundary_condition, 
               L):

    # Save interval
    save_interval = 1000
    save_points = int(number_of_steps/save_interval)

    # Store data
    x_arr = np.zeros((save_points, number_of_particles))
    y_arr = np.zeros((save_points, number_of_particles))
    theta_arr = np.zeros((save_points, number_of_particles))
    pred_x_arr = np.zeros((save_points, 1))
    pred_y_arr = np.zeros((save_points, 1))
    pred_theta_arr = np.zeros((save_points, 1))
    eatings = []
    passed_time = 0

    # Prey starting parameters
    x, y, theta = calculate_prey_starting_parameters(number_of_particles, setup)
    x_arr[0], y_arr[0], theta_arr[0] = x, y, theta

    # Predator starting parameters
    pred_x, pred_y, pred_theta = calculate_predator_starting_parameters_outside_box()
    pred_x_arr[0], pred_y_arr[0], pred_theta_arr[0] = pred_x, pred_y, pred_theta

    for step in tqdm(range(1,number_of_steps), desc='Running simulation', unit='timestep'):

        # Save variables
        if step % save_interval == 0:
            i = int(step / save_interval)
            x_arr[i] = np.copy(x)
            y_arr[i] = np.copy(y)
            theta_arr[i] = np.copy(theta)
            pred_x_arr[i] = np.copy(pred_x)
            pred_y_arr[i] = np.copy(pred_y)
            pred_theta_arr[i] = np.copy(pred_theta)

        # Clock
        passed_time += dt

        # Calculate movement change
        wca = WCA(x, y, number_of_particles, boundary_condition)
        x += v0 * np.cos(theta) * dt + np.sqrt(2 * D * dt) * np.random.randn(number_of_particles) + mu * wca[0] * dt
        y += v0 * np.sin(theta) * dt + np.sqrt(2 * D * dt) * np.random.randn(number_of_particles) + mu * wca[1] * dt

        pred_x += (v_pred * np.cos(pred_theta) * dt + np.sqrt(2 * D * dt) * np.random.randn(1))
        pred_y += (v_pred * np.sin(pred_theta) * dt + np.sqrt(2 * D * dt) * np.random.randn(1))

        theta += mu_r * det_T(x, y, theta, pred_x, pred_y, pred_theta, number_of_particles, boundary_condition, T_A, T_0, R_prey, R_prey_pred) * dt + np.sqrt(2 * D_rot * dt) * np.random.randn(number_of_particles)

        T_P_j, x, eating_count = det_pred_T(x, y, pred_x, pred_y, pred_theta, T_0_predator, R_pred_prey, boundary_condition)
        for i in range(eating_count):
            eatings.append(passed_time)

        pred_theta += mu_r * T_P_j * dt + np.sqrt(2 * D_rot * dt) * np.random.randn(1)

        # Introduce predator
        if step == predator_introduction_step:
            pred_x, pred_y, pred_theta = calculate_predator_starting_parameters_in_box(x, y, number_of_particles, R_pred_prey)

        # Apply boundary condition
        if boundary_condition:

            x = np.where(x > L, x - L, np.where(x < 0, x + L, x))
            y = np.where(y > L, y - L, np.where(y < 0, y + L, y))
            pred_x = np.where(pred_x > L, pred_x - L, np.where(pred_x < 0, pred_x + L, pred_x))
            pred_y = np.where(pred_y > L, pred_y - L, np.where(pred_y < 0, pred_y + L, pred_y))


    return (np.array([x_arr, y_arr]), np.array([pred_x_arr, pred_y_arr]), np.array(eatings))