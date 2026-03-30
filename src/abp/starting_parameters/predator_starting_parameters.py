import numpy as np

def calculate_predator_starting_parameters_in_box(x, y, number_of_particles, R_pred_prey):

    pred_x = np.array([np.sum(x) / number_of_particles])
    pred_y = np.array([np.sum(y) / number_of_particles - R_pred_prey])
    pred_theta = np.array([np.pi/2])

    return pred_x, pred_y, pred_theta

def calculate_predator_starting_parameters_outside_box():

    pred_x = np.random.uniform(80000000, 81000000, 1)
    pred_y = np.random.uniform(80000000, 81000000, 1)
    pred_theta = np.random.uniform(np.pi / 4, np.pi / 4, 1)

    return pred_x, pred_y, pred_theta